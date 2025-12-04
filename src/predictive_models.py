"""
Predictive models for market analysis
Includes Linear Regression (GDP prediction) and Logistic Regression (market classification)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns


class GDPPredictor:
    """Linear Regression model to predict GDP per capita"""

    def __init__(self):
        self.model = LinearRegression()
        self.features = [
            "Literacy (%)",
            "Phones (per 1000)",
            "Birthrate",
            "Infant mortality (per 1000 births)",
        ]
        self.is_trained = False

    def train(self, data):
        """Train the linear regression model"""
        df = data.copy()

        # Prepare features and target
        X = df[self.features].copy()
        y = df["GDP ($ per capita)"].copy()

        # Remove rows with missing values
        mask = X.notna().all(axis=1) & y.notna()
        X = X[mask]
        y = y[mask]

        if len(X) < 10:
            print("Warning: Not enough data to train GDP predictor")
            return None

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        results = {
            "r2_score": r2,
            "coefficients": dict(zip(self.features, self.model.coef_)),
            "intercept": self.model.intercept_,
            "X_test": X_test,
            "y_test": y_test,
            "y_pred": y_pred,
        }

        return results

    def predict(self, features_dict):
        """Predict GDP for given features"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X = pd.DataFrame([features_dict])[self.features]
        return self.model.predict(X)[0]

    def plot_results(self, results):
        """Plot actual vs predicted GDP"""
        if results is None:
            return

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Actual vs Predicted
        axes[0].scatter(results["y_test"], results["y_pred"], alpha=0.6)
        axes[0].plot(
            [results["y_test"].min(), results["y_test"].max()],
            [results["y_test"].min(), results["y_test"].max()],
            "r--",
            lw=2,
        )
        axes[0].set_xlabel("Actual GDP per Capita")
        axes[0].set_ylabel("Predicted GDP per Capita")
        axes[0].set_title(f'GDP Prediction (R² = {results["r2_score"]:.3f})')
        axes[0].grid(True, alpha=0.3)

        # Feature Importance
        coef_abs = np.abs(list(results["coefficients"].values()))
        features = list(results["coefficients"].keys())
        axes[1].barh(features, coef_abs)
        axes[1].set_xlabel("Absolute Coefficient Value")
        axes[1].set_title("Feature Importance (Linear Regression)")
        axes[1].grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        plt.savefig("gdp_prediction_results.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("✓ Saved: gdp_prediction_results.png")


class MarketClassifier:
    """Logistic Regression to classify high-potential markets"""

    def __init__(self):
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.features = [
            "Literacy (%)",
            "Phones (per 1000)",
            "Birthrate",
            "Infant mortality (per 1000 births)",
        ]
        self.is_trained = False

    def train(self, data):
        """Train the logistic regression model"""
        df = data.copy()

        # Create binary target: High MOS (above median)
        if "MOS" not in df.columns:
            print("Warning: MOS not calculated. Cannot train classifier.")
            return None

        median_mos = df["MOS"].median()
        df["High_MOS"] = (df["MOS"] >= median_mos).astype(int)

        # Prepare features and target
        X = df[self.features].copy()
        y = df["High_MOS"].copy()

        # Remove rows with missing values
        mask = X.notna().all(axis=1)
        X = X[mask]
        y = y[mask]

        if len(X) < 10:
            print("Warning: Not enough data to train market classifier")
            return None

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        results = {
            "accuracy": acc,
            "confusion_matrix": cm,
            "classification_report": classification_report(y_test, y_pred),
            "fpr": fpr,
            "tpr": tpr,
            "roc_auc": roc_auc,
            "y_test": y_test,
            "y_pred": y_pred,
            "y_prob": y_prob,
        }

        return results

    def predict_probability(self, features_dict):
        """Predict probability of being a high-potential market"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X = pd.DataFrame([features_dict])[self.features]
        return self.model.predict_proba(X)[0][1]

    def plot_results(self, results):
        """Plot confusion matrix and ROC curve"""
        if results is None:
            return

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Confusion Matrix
        sns.heatmap(
            results["confusion_matrix"],
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=axes[0],
            cbar=False,
        )
        axes[0].set_xlabel("Predicted")
        axes[0].set_ylabel("Actual")
        axes[0].set_title(f'Confusion Matrix (Acc = {results["accuracy"]:.3f})')
        axes[0].set_xticklabels(["Low MOS", "High MOS"])
        axes[0].set_yticklabels(["Low MOS", "High MOS"])

        # ROC Curve
        axes[1].plot(
            results["fpr"],
            results["tpr"],
            label=f'AUC = {results["roc_auc"]:.3f}',
            lw=2,
        )
        axes[1].plot([0, 1], [0, 1], "r--", lw=2, label="Random")
        axes[1].set_xlabel("False Positive Rate")
        axes[1].set_ylabel("True Positive Rate")
        axes[1].set_title("ROC Curve - Market Classification")
        axes[1].legend(loc="lower right")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("market_classification_results.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("✓ Saved: market_classification_results.png")
