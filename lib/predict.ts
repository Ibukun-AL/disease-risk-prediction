import model from "./model.json";

export const N_FEATURES = model.features.length; // 30
export const FEATURE_NAMES: string[] = model.features;

export type Prediction = { risk: number; label: "higher" | "lower" };

// Same maths as scikit-learn's StandardScaler followed by LogisticRegression.
export function predict(features: number[]): Prediction {
  let z = model.intercept;
  for (let i = 0; i < N_FEATURES; i++) {
    z += ((features[i] - model.mean[i]) / model.scale[i]) * model.coef[i];
  }
  const risk = z >= 0 ? 1 / (1 + Math.exp(-z)) : Math.exp(z) / (1 + Math.exp(z)); // stable sigmoid
  return { risk, label: risk >= 0.5 ? "higher" : "lower" };
}

export type Validation = { ok: true; features: number[] } | { ok: false; error: string };

export function validateFeatures(input: unknown): Validation {
  if (!Array.isArray(input) || input.length !== N_FEATURES) return { ok: false, error: `Expected ${N_FEATURES} numbers.` };
  if (!input.every((x) => typeof x === "number" && Number.isFinite(x))) return { ok: false, error: "Every value must be a finite number." };
  return { ok: true, features: input as number[] };
}
