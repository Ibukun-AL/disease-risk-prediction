import { describe, expect, it } from "vitest";
import model from "../model.json";
import parity from "./fixtures/parity.json";
import { predict, validateFeatures, N_FEATURES } from "../predict";

describe("predict", () => {
  it("matches scikit-learn's probabilities on held-out rows", () => {
    for (const row of parity) {
      expect(predict(row.features).risk).toBeCloseTo(row.risk, 9);
    }
  });

  it("labels the high-risk example 'higher' and the low-risk example 'lower'", () => {
    expect(predict(model.examples.higher).label).toBe("higher");
    expect(predict(model.examples.lower).label).toBe("lower");
  });

  it("returns a risk between 0 and 1 even for extreme inputs", () => {
    const huge = Array(N_FEATURES).fill(1e9);
    const r = predict(huge).risk;
    expect(r).toBeGreaterThanOrEqual(0);
    expect(r).toBeLessThanOrEqual(1);
  });
});

describe("validateFeatures", () => {
  it("accepts exactly 30 finite numbers", () => {
    expect(validateFeatures(model.examples.higher)).toEqual({ ok: true, features: model.examples.higher });
  });
  it("rejects the wrong length", () => {
    expect(validateFeatures([1, 2, 3])).toEqual({ ok: false, error: "Expected 30 numbers." });
  });
  it("rejects non-numbers and non-finite values", () => {
    const bad = [...model.examples.higher];
    bad[4] = Number.NaN;
    expect(validateFeatures(bad).ok).toBe(false);
    expect(validateFeatures("nope" as unknown).ok).toBe(false);
  });
});
