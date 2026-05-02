import time

import numpy as np
from sklearn.ensemble import IsolationForest

from defense.defense import block_ip
from detection.feature_extractor import extract_features


def prepare_data(features):
    data = []

    for feature in features:
        data.append(
            [
                feature["total_requests"],
                feature["failed_logins"],
                feature["success_logins"],
                feature["unique_paths"],
                feature["request_rate"],
            ]
        )

    return np.array(data)


def train_model(data):
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(data)
    return model


def detect_anomalies(model, data):
    predictions = model.predict(data)
    return ["ATTACK" if prediction == -1 else "NORMAL" for prediction in predictions]


def rule_based_label(feature):
    return "ATTACK" if feature.get("request_rate", 0) > 5 or feature.get("failed_logins", 0) > 10 else "NORMAL"


def label_features(features):
    if not features:
        return []

    labeled_features = [dict(feature) for feature in features]

    if len(labeled_features) < 2:
        for feature in labeled_features:
            feature["label"] = rule_based_label(feature)
            feature["detection_method"] = "rules"
        return labeled_features

    data = prepare_data(labeled_features)
    model = train_model(data)
    labels = detect_anomalies(model, data)

    for index, label in enumerate(labels):
        feature = labeled_features[index]
        rule_label = rule_based_label(feature)

        feature["label"] = "ATTACK" if label == "ATTACK" or rule_label == "ATTACK" else "NORMAL"
        feature["ml_label"] = label
        feature["rule_label"] = rule_label
        feature["detection_method"] = "ml+rules"

    return labeled_features


if __name__ == "__main__":
    model = None

    while True:
        print("\n[ML SCAN RUNNING]")

        features = extract_features()

        if len(features) < 2:
            print("Not enough data yet...")
            time.sleep(1)
            continue

        labeled_features = label_features(features)
        data = prepare_data(labeled_features)

        if model is None:
            model = train_model(data)
            print("[MODEL TRAINED]")

        results = detect_anomalies(model, data)

        for index, result in enumerate(results):
            ip = labeled_features[index]["ip"]

            print(ip, "->", result)

            if result == "ATTACK":
                block_ip(ip)

        time.sleep(1)
