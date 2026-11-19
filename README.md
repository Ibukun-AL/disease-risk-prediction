# Disease risk prediction

Personal project by Ibukun Aluko. A Next.js app that scores 30 tumour measurements with a logistic regression trained in Python on a public dataset, with a form for people and a JSON API for programs.

**Not medical advice.** The model is trained on scikit-learn's bundled Breast Cancer Wisconsin (Diagnostic) dataset for demonstration only. It is inspired by my MSc and IEEE research on disease prediction but does not use that research data.

## How it works

1. **Train (Python).** `training/train.py` fits a scaler and a logistic regression, reports held-out accuracy (96.5%), and exports the fitted numbers to `lib/model.json`.
2. **Serve (TypeScript).** `lib/predict.ts` applies the same maths (scale, weighted sum, sigmoid), so the app deploys on Vercel with no Python runtime.
3. **Prove it matches.** The export also writes held-out rows with scikit-learn's own probabilities. A test checks the TypeScript predictor agrees with them to 9 decimal places.
4. **Validate.** The API returns 422 unless it gets exactly 30 finite numbers, and 400 for a body that is not JSON.

## Run it

```bash
npm install
npm run dev
```

```bash
curl -X POST localhost:3000/api/predict -H 'content-type: application/json' \
  -d '{"features":[17.99,10.38,122.8,1001,0.1184,0.2776,0.3001,0.1471,0.2419,0.07871,1.095,0.9053,8.589,153.4,0.006399,0.04904,0.05373,0.01587,0.03003,0.006193,25.38,17.33,184.6,2019,0.1622,0.6656,0.7119,0.2654,0.4601,0.1189]}'
```

## Retrain

```bash
cd training
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python train.py
```

## Tests

```bash
npm test
```

9 Vitest tests cover parity with scikit-learn, labels, extreme inputs, validation and the API route.
