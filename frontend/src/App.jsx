import { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, Radio, ShieldAlert, ShieldCheck, WifiOff } from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  Filler,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './App.css';
import gabrixLogo from './assets/gabrix-logo-dark.png';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler);

const getSocketUrl = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const apiHost = import.meta.env.VITE_API_HOST || '127.0.0.1:8000';
  return `${protocol}//${apiHost}/ws`;
};

const App = () => {
  const [features, setFeatures] = useState([]);
  const [blockedIps, setBlockedIps] = useState([]);
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });
  const [connectionState, setConnectionState] = useState('connecting');
  const wsRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(getSocketUrl());
    wsRef.current = socket;

    socket.onopen = () => setConnectionState('connected');
    socket.onclose = () => setConnectionState('disconnected');
    socket.onerror = () => setConnectionState('disconnected');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const nextFeatures = data.features || [];
      setFeatures(nextFeatures);
      setBlockedIps(data.blocked_ips || []);

      const totalRequests = nextFeatures.reduce((sum, feature) => sum + feature.total_requests, 0);
      const time = new Date().toLocaleTimeString();

      setChartData((previous) => {
        const labels = [...(previous.labels || []), time].slice(-15);
        const traffic = [...(previous.datasets?.[0]?.data || []), totalRequests].slice(-15);

        return {
          labels,
          datasets: [
            {
              label: 'Total Traffic',
              data: traffic,
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.18)',
              fill: true,
              tension: 0.35,
              pointRadius: 2,
            },
          ],
        };
      });
    };

    return () => socket.close();
  }, []);

  const totals = useMemo(() => {
    return features.reduce(
      (summary, feature) => ({
        requests: summary.requests + feature.total_requests,
        failed: summary.failed + feature.failed_logins,
        attacks: summary.attacks + (feature.label === 'ATTACK' ? 1 : 0),
      }),
      { requests: 0, failed: 0, attacks: 0 },
    );
  }, [features]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: { color: '#94a3b8', precision: 0 },
        grid: { color: 'rgba(148, 163, 184, 0.14)' },
      },
      x: {
        ticks: { color: '#94a3b8', maxRotation: 0 },
        grid: { color: 'rgba(148, 163, 184, 0.08)' },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#0f172a',
        borderColor: '#334155',
        borderWidth: 1,
      },
    },
  };

  return (
    <main className="app-shell">
      <section className="hero-band">
        <div>
          <p className="eyebrow">Live Cyber Defense Simulator</p>
          <h1>Cyber Command Center</h1>
        </div>
        <div className={`connection-pill ${connectionState}`}>
          {connectionState === 'connected' ? <Radio size={18} /> : <WifiOff size={18} />}
          <span>{connectionState}</span>
        </div>
      </section>

      <section className="metric-grid" aria-label="Traffic summary">
        <article className="metric">
          <Activity size={22} />
          <span>Total Requests</span>
          <strong>{totals.requests}</strong>
        </article>
        <article className="metric">
          <ShieldAlert size={22} />
          <span>Attack Signals</span>
          <strong>{totals.attacks}</strong>
        </article>
        <article className="metric">
          <ShieldCheck size={22} />
          <span>Blocked IPs</span>
          <strong>{blockedIps.length}</strong>
        </article>
      </section>

      <section className="dashboard-grid">
        <article className="panel traffic-panel">
          <div className="panel-heading">
            <h2>Live Traffic Volume</h2>
            <span>Last 15 samples</span>
          </div>
          <div className="chart-frame">
            {chartData.labels.length > 0 ? (
              <Line data={chartData} options={chartOptions} />
            ) : (
              <div className="empty-state">Waiting for traffic</div>
            )}
          </div>
        </article>

        <article className="panel">
          <div className="panel-heading danger">
            <h2>Threat Defense</h2>
            <span>Auto blocked</span>
          </div>
          <div className="blocked-list">
            {blockedIps.length === 0 && <div className="empty-state compact">No active blocks</div>}
            {blockedIps.map((ip) => (
              <div className="blocked-row" key={ip}>
                <span>{ip}</span>
                <strong>Blocked</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="panel connections-panel">
          <div className="panel-heading">
            <h2>Active Connections</h2>
            <span>{features.length} observed IPs</span>
          </div>
          <div className="connection-grid">
            {features.length === 0 && <div className="empty-state">Awaiting incoming connections</div>}
            {features.map((feature) => {
              const isAttack = feature.label === 'ATTACK';

              return (
                <div className={`connection-card ${isAttack ? 'attack' : 'normal'}`} key={feature.ip}>
                  <div className="connection-card-header">
                    <strong>{feature.ip}</strong>
                    <span>{isAttack ? 'Attack' : 'Normal'}</span>
                  </div>
                  <dl>
                    <div>
                      <dt>Requests</dt>
                      <dd>{feature.total_requests}</dd>
                    </div>
                    <div>
                      <dt>Failed</dt>
                      <dd>{feature.failed_logins}</dd>
                    </div>
                    <div>
                      <dt>Rate</dt>
                      <dd>{feature.request_rate.toFixed(2)} req/s</dd>
                    </div>
                    <div>
                      <dt>Detection</dt>
                      <dd>{feature.detection_method || 'rules'}</dd>
                    </div>
                  </dl>
                </div>
              );
            })}
          </div>
        </article>
      </section>

      <footer className="gabrix-stage" aria-label="GABRIX lab identity">
        <motion.img
          alt="GABRIX"
          className="gabrix-logo"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          src={gabrixLogo}
          whileHover={{ y: -3, scale: 1.02 }}
          transition={{ duration: 0.45, ease: 'easeOut' }}
        />
      </footer>
    </main>
  );
};

export default App;
