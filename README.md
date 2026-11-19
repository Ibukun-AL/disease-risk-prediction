# Risk prediction service

Personal project by Ibukun Aluko. A Spring Boot REST gateway in front of a Python (FastAPI + scikit-learn) model, containerised with Docker and tested in CI.

**Not medical advice.** The model is trained on scikit-learn's bundled public Breast Cancer Wisconsin dataset for demonstration only. It is inspired by my MSc and IEEE research on disease prediction but does not use that research data.

## Run

```bash
docker compose up --build
curl -X POST localhost:8080/api/v1/risk -H 'content-type: application/json' \
  -d '{"features":[17.99,10.38,122.8,1001,0.1184,0.2776,0.3001,0.1471,0.2419,0.07871,1.095,0.9053,8.589,153.4,0.006399,0.04904,0.05373,0.01587,0.03003,0.006193,25.38,17.33,184.6,2019,0.1622,0.6656,0.7119,0.2654,0.4601,0.1189]}'
```

API docs: `localhost:8080/swagger-ui.html`.

## Tests

- Model: `cd model && python train.py && pytest`
- Gateway: `cd gateway && mvn test`

If the model service is down the gateway returns `503 {"error":"model service unavailable"}`.
