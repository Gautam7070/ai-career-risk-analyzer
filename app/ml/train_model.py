import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load dataset
df = pd.read_csv("dataset/ai_job_trends_dataset.csv")

# 2. Clean column names
df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("%", "percent")
)

# 3. Convert AI impact level to numeric
ai_impact_mapping = {
    "Low": 0,
    "Moderate": 1,
    "High": 2
}
df["ai_impact_level"] = df["ai_impact_level"].map(ai_impact_mapping)

# 4. Select features & target
features = [
    "experience_required_years",
    "ai_impact_level",
    "projected_openings_2030",
    "remote_work_ratio_percent"
]

target = "automation_risk_percent"

# 5. Handle missing values
df[features] = df[features].fillna(df[features].median())
df[target] = df[target].fillna(df[target].median())

# 6. Train-test split
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# 8. Evaluate model
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation")
print("MAE:", mae)
print("R2 Score:", r2)

# 9. Save model
joblib.dump(model, "models/automation_risk_model.pkl")
print("Model saved successfully!")
