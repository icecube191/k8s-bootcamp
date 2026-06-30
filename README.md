# Kubernetes Bootcamp — FastAPI + PostgreSQL on K8s

A production-style Kubernetes deployment of a FastAPI task management API backed by PostgreSQL, built as part of a hands-on K8s learning bootcamp.

## Stack

- **FastAPI** (Python) — REST API with async PostgreSQL access via asyncpg
- **PostgreSQL 16** — deployed as a StatefulSet with persistent storage
- **Helm** — chart-based deployment with templated values
- **ArgoCD** — GitOps continuous deployment, auto-syncs from this repo
- **GitHub Actions** — CI pipeline builds and pushes Docker images to GHCR on every push to main
- **NGINX Ingress** — routes external traffic to the API

## Architecture

GitHub Push → GitHub Actions (build + push image to GHCR)

↓

ArgoCD detects new image tag in values.yaml

↓

Helm chart synced to Kubernetes cluster

↓

[Ingress] → [task-api Deployment] → [postgres StatefulSet]
## Project Structure

├── app/                        # FastAPI application code

├── helm/task-api/              # Helm chart

│   ├── Chart.yaml

│   ├── values.yaml

│   └── templates/              # K8s manifests (templatized)

├── k8s/                        # Raw kubectl manifests (reference)

├── .github/workflows/ci.yml    # GitHub Actions CI pipeline

├── Dockerfile

└── argocd-app.yaml             # ArgoCD Application definition

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /api/tasks | List all tasks |
| POST | /api/tasks | Create a task |
| PATCH | /api/tasks/{id} | Mark task complete |

## Local Development

```bash
# Build image
docker build -t task-api:local .

# Deploy to local K8s (Docker Desktop)
helm install task-api ./helm/task-api \
  --namespace bootcamp2 \
  --create-namespace \
  --set postgres.password="your-password"

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## Key Concepts Demonstrated

- StatefulSet with persistent volumes for database
- Kubernetes Secrets for credential management
- Helm chart templating with values override
- GitOps workflow with ArgoCD auto-sync and self-heal
- CI/CD pipeline with automatic image tagging and Helm values update
- Headless service + ClusterIP service pattern for StatefulSets
- Readiness and liveness probes
- Resource requests and limits