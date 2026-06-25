# Notes App

A production-style notes API built with FastAPI, containerised 
with Docker, deployed on Kubernetes, and monitored with Grafana.

## Architecture
- FastAPI — REST API with 3 endpoints
- PostgreSQL — persistent database
- Docker + docker-compose — containerisation
- Kubernetes (k3d) — orchestration with 2 replicas
- Prometheus + Grafana — monitoring and dashboards

## API Routes
- GET / — health check
- POST /notes — create a note
- GET /notes — list all notes
- DELETE /notes/{id} — delete a note

## Run locally with Docker
docker build -t notes-api .
docker run -p 8000:8000 notes-api

## Run with docker-compose (with Postgres)
docker-compose up --build

## Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/postgres.yaml

## Monitoring
Prometheus + Grafana installed via Helm.
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
Open localhost:3000 — admin / admin123

## Tech Stack
Python · FastAPI · PostgreSQL · Docker · Kubernetes · 
Prometheus · Grafana · Helm