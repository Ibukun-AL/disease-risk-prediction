"use client";
import { useState } from "react";
import model from "@/lib/model.json";
import s from "@/app/page.module.css";

const GROUPS = ["Mean", "Error", "Worst"] as const;
const per = model.features.length / GROUPS.length; // 10 measurements, three ways
const blank = () => Array<string>(model.features.length).fill("");
const label = (name: string) => name.replace(/^(mean|worst) /, "").replace(/ error$/, "").replace(/^\w/, (c) => c.toUpperCase());

type Result = { risk: number; label: "higher" | "lower" };

export default function Predictor() {
  const [vals, setVals] = useState<string[]>(blank());
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const load = (row: number[]) => { setVals(row.map(String)); setResult(null); setError(null); };

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true); setError(null); setResult(null);
    try {
      const res = await fetch("/api/predict", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ features: vals.map((v) => (v.trim() === "" ? NaN : Number(v))).map((n) => (Number.isFinite(n) ? n : null)) }) });
      const data = await res.json();
      if (!res.ok) setError(res.status === 422 ? "Fill in all 30 values with numbers, or load an example." : data.error ?? "Something went wrong.");
      else setResult(data);
    } catch {
      setError("Couldn't reach the server.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className={s.form}>
      <div className={s.row}>
        <button type="button" className={s.ghost} onClick={() => load(model.examples.higher)}>Load higher-risk example</button>
        <button type="button" className={s.ghost} onClick={() => load(model.examples.lower)}>Load lower-risk example</button>
        <button type="button" className={s.ghost} onClick={() => { setVals(blank()); setResult(null); setError(null); }}>Clear</button>
      </div>

      <div className={s.cols}>
        {GROUPS.map((g, gi) => (
          <fieldset key={g} className={s.group}>
            <legend>{g}</legend>
            {model.features.slice(gi * per, gi * per + per).map((name, i) => {
              const idx = gi * per + i;
              return (
                <label key={name} className={s.field}>
                  <span>{label(name)}</span>
                  <input inputMode="decimal" value={vals[idx]} onChange={(e) => setVals(vals.map((v, j) => (j === idx ? e.target.value : v)))} />
                </label>
              );
            })}
          </fieldset>
        ))}
      </div>

      <div className={s.row}>
        <button className={s.go} disabled={busy}>{busy ? "Scoring…" : "Predict risk"}</button>
        {error && <p role="alert" className={s.error}>{error}</p>}
      </div>

      <div aria-live="polite">
        {result && (
          <section className={s.result}>
            <p className={s.big}>{(result.risk * 100).toFixed(1)}%</p>
            <p>Model risk score. Classed as <strong>{result.label}</strong> risk.</p>
            <div className={s.meter} aria-hidden="true"><span style={{ width: `${result.risk * 100}%` }} /></div>
          </section>
        )}
      </div>
    </form>
  );
}
