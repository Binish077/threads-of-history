# threads-of-history
history simulator platform

## Run the backend

```bash
source .venv/bin/activate
uvicorn app.main:app --app-dir backend --reload
```

The API is available at `http://127.0.0.1:8000`. Check the service with:

```bash
curl http://127.0.0.1:8000/health
```

Run the backend tests with:

```bash
pytest backend/tests
```
