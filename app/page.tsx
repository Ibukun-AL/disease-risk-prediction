import model from "@/lib/model.json";
import Predictor from "@/components/Predictor";
import s from "./page.module.css";

export default function Page() {
  return (
    <main className={s.main}>
      <span className={s.k}>Personal project · Next.js and Python</span>
      <h1 className={s.h1}>Disease risk prediction</h1>
      <p className={s.lede}>
        A logistic regression trained in Python on a public dataset ({model.dataset}), then served from this app&apos;s own API.
        Held-out accuracy {(model.heldOutAccuracy * 100).toFixed(1)}%. Load an example row or type your own 30 measurements.
      </p>
      <Predictor />
      <p className={s.note}>
        Not medical advice. A demonstration built on a public dataset; it does not use any unpublished research data.
        The same model is available as <code>POST /api/predict</code> with <code>{`{"features": [30 numbers]}`}</code>.
      </p>
    </main>
  );
}
