import { describe, expect, it } from "vitest";
import model from "../model.json";
import { POST } from "../../app/api/predict/route";

const call = (body: string) => POST(new Request("http://x.test/api/predict", { method: "POST", body, headers: { "content-type": "application/json" } }));

describe("POST /api/predict", () => {
  it("returns a risk and label for 30 numbers", async () => {
    const res = await call(JSON.stringify({ features: model.examples.higher }));
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.label).toBe("higher");
    expect(data.risk).toBeGreaterThan(0.5);
  });
  it("returns 422 for the wrong number of values", async () => {
    expect((await call(JSON.stringify({ features: [1, 2] }))).status).toBe(422);
  });
  it("returns 400 for a body that is not JSON", async () => {
    expect((await call("not json")).status).toBe(400);
  });
});
