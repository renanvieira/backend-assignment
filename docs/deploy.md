# Deployment & Operations

## 1. Containerization
The application is packaged as a Docker image for portability across environments (ECS, Lambda, or local).

**Build:**
```bash
docker build -t tiqets-assignment .
```

**Run (with persistent output):**
```bash
docker run --rm -v "$(pwd)/data:/app/data" tiqets-assignment
```

## 2. Automation
As a batch process, the container should be triggered via a **Cron job** or **Systemd Timer** after daily upstream exports are finalized.

## 3. Observability
- **Exit Codes**: The script returns `1` on critical failure (missing files, malformed headers) to trigger infrastructure alerts.
- **Logging**: Validation warnings are sent to `stderr` for audit and ingestion into log aggregators (e.g., CloudWatch, Datadog).
