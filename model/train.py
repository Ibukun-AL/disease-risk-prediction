"""Train a logistic regression on scikit-learn's bundled Breast Cancer Wisconsin dataset.

Public dataset, bundled with scikit-learn. Demonstration only, not medical advice.
"""
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    data = load_breast_cancer()
    # target 0 = malignant, 1 = benign. Flip so 1 means the higher-risk class.
    y = 1 - data.target
    X_train, X_test, y_train, y_test = train_test_split(data.data, y, test_size=0.2, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    model.fit(X_train, y_train)
    print(f"held-out accuracy: {model.score(X_test, y_test):.3f}")
    joblib.dump(model, "model.pkl")
