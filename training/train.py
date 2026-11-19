"""Train a logistic regression on scikit-learn's bundled Breast Cancer Wisconsin dataset and export it.

Public dataset, bundled with scikit-learn. Demonstration only, not medical advice.

Writes, for the Next.js app:
  ../lib/model.json                      scaler + coefficients + metadata + two example rows
  ../lib/__tests__/fixtures/parity.json  held-out rows with scikit-learn's own probabilities,
                                         so the TypeScript predictor can be checked against it
"""
import json
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parent.parent / "lib"

if __name__ == "__main__":
    data = load_breast_cancer()
    # target 0 = malignant, 1 = benign. Flip so 1 means the higher-risk class.
    y = 1 - data.target
    X_train, X_test, y_train, y_test = train_test_split(data.data, y, test_size=0.2, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    model.fit(X_train, y_train)
    accuracy = float(model.score(X_test, y_test))
    print(f"held-out accuracy: {accuracy:.3f}")

    scaler, clf = model[0], model[1]
    higher = next(x for x, t in zip(X_test, y_test) if t == 1)
    lower = next(x for x, t in zip(X_test, y_test) if t == 0)

    OUT.mkdir(exist_ok=True)
    (OUT / "model.json").write_text(json.dumps({
        "dataset": "Breast Cancer Wisconsin (Diagnostic), bundled with scikit-learn",
        "heldOutAccuracy": round(accuracy, 3),
        "features": list(data.feature_names),
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "coef": clf.coef_[0].tolist(),
        "intercept": float(clf.intercept_[0]),
        "examples": {"higher": higher.tolist(), "lower": lower.tolist()},
    }, indent=1))

    fixtures = OUT / "__tests__" / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    rows = X_test[:12]
    probs = model.predict_proba(rows)[:, 1]
    (fixtures / "parity.json").write_text(json.dumps(
        [{"features": r.tolist(), "risk": float(p)} for r, p in zip(rows, probs)], indent=1))
    print(f"wrote {OUT / 'model.json'} and parity fixtures")
