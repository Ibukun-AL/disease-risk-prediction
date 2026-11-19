from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

N_FEATURES = 30
app = FastAPI(title="Risk model service")
_model = joblib.load(Path(__file__).parent / "model.pkl")


class PredictIn(BaseModel):
    features: list[float] = Field(min_length=N_FEATURES, max_length=N_FEATURES)


@app.get("/health")
def health():
    return {"status": "ok"}


_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Risk model service</title>
<style>
*{box-sizing:border-box;margin:0}body{font:16px/1.55 system-ui,sans-serif;background:#0f1b22;color:#e6eef0}
main{max-width:52rem;margin:0 auto;padding:3rem 1.25rem}
.k{color:#7fb7c2;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700}
h1{font-size:2.3rem;line-height:1.1;margin:.5rem 0 .75rem;letter-spacing:-.02em}
p{color:#b4c7cc;max-width:40rem}.row{display:flex;gap:.6rem;flex-wrap:wrap;margin:1.25rem 0}
.pill{border:1px solid #2d4852;border-radius:99px;padding:.25rem .8rem;font-size:.85rem;color:#cfe3e7}
.ok{color:#7be0a9}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.5rem}
.card{background:#16272f;border:1px solid #2d4852;border-radius:10px;padding:1rem 1.1rem}
.card h2{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:#7fb7c2;margin-bottom:.6rem}
pre{font:13px/1.5 ui-monospace,Menlo,monospace;color:#e6eef0;white-space:pre-wrap;word-break:break-word}
.m{font:600 .8rem ui-monospace,monospace;color:#0f1b22;background:#7be0a9;border-radius:4px;padding:.1rem .4rem;margin-right:.4rem}
.big{font-size:2.6rem;font-weight:800;letter-spacing:-.02em}
a{color:#7fb7c2}.note{margin-top:1.5rem;font-size:.85rem;color:#8fa6ab}
@media(max-width:640px){.grid{grid-template-columns:1fr}}
</style></head><body><main>
<span class="k">Personal project · Python model service</span>
<h1>Risk model service</h1>
<p>A logistic regression on a public dataset (Breast Cancer Wisconsin, bundled with scikit-learn). The Spring Boot gateway calls this service; this page is its status board.</p>
<div class="row"><span class="pill"><span class="ok">●</span> status: ok</span><span class="pill">held-out accuracy 96.5%</span><span class="pill">30 input features</span><a class="pill" href="/docs">API docs</a></div>
<div class="grid">
<div class="card"><h2><span class="m">POST</span>/predict</h2><pre>{"features": [30 numbers]}</pre>
<p style="margin-top:.8rem;font-size:.9rem">Returns a risk between 0 and 1 and a label, for example:</p><pre>{"risk": __RISK__, "label": "__LABEL__"}</pre></div>
<div class="card"><h2>Two rows from the public dataset</h2>
<p style="font-size:.9rem">Labelled malignant in the dataset</p><div class="big">__PCT__%</div>
<p style="font-size:.9rem;margin-top:.6rem">Labelled benign in the dataset</p><div class="big">__PCT2__%</div>
<p style="font-size:.8rem;margin-top:.6rem">Scored live by the model when this page loaded.</p></div>
</div>
<p class="note">Not medical advice. A demonstration built on a public dataset; it does not use any unpublished research data.</p>
</main></body></html>"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    from sklearn.datasets import load_breast_cancer

    data = load_breast_cancer()
    malignant = data.data[list(data.target).index(0)].tolist()
    benign = data.data[list(data.target).index(1)].tolist()
    r1 = float(_model.predict_proba([malignant])[0][1])
    r2 = float(_model.predict_proba([benign])[0][1])
    return (
        _PAGE.replace("__RISK__", f"{r1:.3f}")
        .replace("__LABEL__", "higher" if r1 >= 0.5 else "lower")
        .replace("__PCT__", f"{r1 * 100:.1f}")
        .replace("__PCT2__", f"{r2 * 100:.1f}")
    )


@app.post("/predict")
def predict(body: PredictIn):
    risk = float(_model.predict_proba([body.features])[0][1])
    return {"risk": risk, "label": "higher" if risk >= 0.5 else "lower"}
