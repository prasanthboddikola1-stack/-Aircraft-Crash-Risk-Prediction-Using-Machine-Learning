import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= LOAD DATA =================
real_file = next(
    f for f in os.listdir(BASE_DIR)
    if f.startswith("Aircraft_Cleaned_Preprocessed") and f.endswith(".xlsx")
)

ml_file = next(
    f for f in os.listdir(BASE_DIR)
    if f.startswith("Aircraft_Cleaned_Standardized") and f.endswith(".xlsx")
)

df_real = pd.read_excel(os.path.join(BASE_DIR, real_file))
df_ml = pd.read_excel(os.path.join(BASE_DIR, ml_file))

# ================= AIRLINE DECODE MAP =================
AIRLINE_MAP = {
    0: "IndiGo",
    1: "Air India",
    2: "SpiceJet",
    3: "Vistara",
    4: "GoAir",
    5: "Alliance Air"
}

# ================= TRAIN MODEL =================
X = df_ml.drop(columns=["Risk_Level_Num"], errors="ignore")
y = df_ml["Risk_Level_Num"]

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)
model.fit(X, y)

RISK_MAP = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}

# ================= PREDICTION FUNCTION =================
def predict_by_record_id(record_id: int):

    if record_id < 0 or record_id >= len(df_real):
        return None

    real = df_real.iloc[record_id]
    ml_row = X.iloc[[record_id]]

    probs = model.predict_proba(ml_row)[0]
    pred = probs.argmax()

    # HIGH risk probability = crash probability
    crash_prob = round(probs[2] * 100, 2)

    return {
        "Airline": AIRLINE_MAP.get(int(real["Airline"]), "Unknown Airline"),
        "Source": real["Source_Airport_Full"],
        "Destination": real["Destination_Airport_Full"],
        "Wind": round(real["Wind_Speed"], 2),
        "Visibility": round(real["Visibility_km"], 2),
        "Storm": "Yes" if real["Storm"] == 1 else "No",
        "Risk_Level": RISK_MAP[pred],
        "Crash_Probability": crash_prob,
    }
