import pandas as pd
import numpy as np

def generate_fake_log(n=1000):
    time = np.arange(n)

    vibe = np.random.normal(10, 2, n)
    voltage = np.linspace(12.6, 11.0, n)

    # Inject issues
    vibe[400:600] += 25
    voltage[700:] -= 2

    df = pd.DataFrame({
        "time": time,
        "vibration": vibe,
        "voltage": voltage
    })

    return df


def analyze(df):
    return {
        "vibration_mean": df["vibration"].mean(),
        "voltage_drop": df["voltage"].iloc[0] - df["voltage"].iloc[-1]
    }


def diagnose(features):
    issues = []

    if features["vibration_mean"] > 20:
        issues.append({
            "issue": "High vibration",
            "evidence": f"Mean vibration = {features['vibration_mean']:.2f}",
            "fix": "Check propellers / frame",
            "confidence": 0.8
        })

    if features["voltage_drop"] > 2:
        issues.append({
            "issue": "Battery drop",
            "evidence": f"Voltage drop = {features['voltage_drop']:.2f}V",
            "fix": "Check battery / wiring",
            "confidence": 0.7
        })

    return issues


if __name__ == "__main__":
    df = generate_fake_log()
    features = analyze(df)
    issues = diagnose(features)

    print("\n--- Flight Diagnostic Report ---\n")

    if not issues:
        print("No issues detected")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['issue']}")
            print(f"   Evidence: {issue['evidence']}")
            print(f"   Fix: {issue['fix']}")
            print(f"   Confidence: {issue['confidence']}\n")