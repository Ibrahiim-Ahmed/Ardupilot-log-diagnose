import pandas as pd
import numpy as np

# -----------------------------
# Fake Log Generator (for now)
# -----------------------------
def generate_fake_log(n=1000):
    time = np.arange(n)

    vibe = np.random.normal(10, 2, n)
    voltage = np.linspace(12.6, 11.0, n)

    # Inject anomalies
    vibe[400:600] += 25
    voltage[700:] -= 2

    df = pd.DataFrame({
        "time": time,
        "vibration": vibe,
        "voltage": voltage
    })

    return df


# -----------------------------
# Feature Analysis
# -----------------------------
def analyze(df):
    return {
        "vibration_mean": df["vibration"].mean(),
        "voltage_drop": df["voltage"].iloc[0] - df["voltage"].iloc[-1]
    }


# -----------------------------
# Time Window Detection
# -----------------------------
def detect_vibration_window(df, threshold=30):
    high = df[df["vibration"] > threshold]

    if high.empty:
        return None

    start = int(high["time"].iloc[0])
    end = int(high["time"].iloc[-1])

    return {
        "start": start,
        "end": end,
        "duration": end - start
    }


def detect_voltage_drop_window(df, threshold=2):
    drop = df["voltage"].iloc[0] - df["voltage"]

    high = df[drop > threshold]

    if high.empty:
        return None

    start = int(high["time"].iloc[0])
    end = int(high["time"].iloc[-1])

    return {
        "start": start,
        "end": end,
        "duration": end - start
    }


# -----------------------------
# Cause Database
# -----------------------------
CAUSE_DB = {
    "High vibration": [
        "Unbalanced propeller",
        "Loose frame",
        "Motor misalignment"
    ],
    "Battery voltage drop": [
        "Weak battery",
        "Power wiring issue",
        "ESC inefficiency"
    ]
}


# -----------------------------
# Diagnosis Engine
# -----------------------------
def diagnose(df, features):
    issues = []

    # Vibration Issue
    vibe_window = detect_vibration_window(df)

    if vibe_window and features["vibration_mean"] > 20:
        issues.append({
            "issue": "High vibration",
            "evidence": [
                f"Mean vibration = {features['vibration_mean']:.2f}",
                f"Duration = {vibe_window['duration']} samples",
                f"Time window = {vibe_window['start']} → {vibe_window['end']}"
            ],
            "causes": CAUSE_DB["High vibration"],
            "fix": "Inspect propellers, motors, and frame stability",
            "confidence": 0.80
        })

    # Battery Issue
    volt_window = detect_voltage_drop_window(df)

    if volt_window and features["voltage_drop"] > 2:
        issues.append({
            "issue": "Battery voltage drop",
            "evidence": [
                f"Voltage drop = {features['voltage_drop']:.2f}V",
                f"Duration = {volt_window['duration']} samples",
                f"Time window = {volt_window['start']} → {volt_window['end']}"
            ],
            "causes": CAUSE_DB["Battery voltage drop"],
            "fix": "Check battery health and power connections",
            "confidence": 0.75
        })

    return issues


# -----------------------------
# Output Formatter
# -----------------------------
def print_report(issues):
    print("\n--- Flight Diagnostic Report ---\n")

    if not issues:
        print("No major issues detected.\n")
        return

    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['issue']}\n")

        print("   Evidence:")
        for ev in issue["evidence"]:
            print(f"   - {ev}")

        print("\n   Possible Causes:")
        for cause in issue["causes"]:
            print(f"   - {cause}")

        print("\n   Suggested Fix:")
        print(f"   {issue['fix']}")

        print(f"\n   Confidence: {issue['confidence']:.2f}")
        print("\n" + "-"*40 + "\n")


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    df = generate_fake_log()

    features = analyze(df)
    issues = diagnose(df, features)

    print_report(issues)