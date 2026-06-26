# Notes App — Production DevOps Stack

A production-style notes API built from scratch, demonstrating
a complete DevOps and Cloud engineering stack.

**GitHub:** github.com/cherry0230/notes-app

---

## What I Built

A REST API for managing notes, used as a vehicle to learn and
demonstrate the full DevOps stack — from local development to
production cloud deployment on AWS EKS.

---

## Architecture

    Browser → AWS Load Balancer → Kubernetes Ingress
           → FastAPI Service → FastAPI Pods (x2)
           → PostgreSQL Database

    Monitoring: Prometheus + Grafana + CloudWatch
    CI/CD: GitHub Actions
    IaC: Terraform
    Registry: AWS ECR


---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Containerisation | Docker, docker-compose |
| Orchestration | Kubernetes (k3d local, EKS production) |
| Infrastructure | Terraform (VPC, Subnet, EC2, EKS) |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana, CloudWatch |
| Registry | AWS ECR |
| Package Manager | Helm |

---

## API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /notes | Create a note |
| GET | /notes | List all notes |
| DELETE | /notes/{id} | Delete a note |

---

## Project Structure

    notes-app/
    ├── main.py                 # FastAPI application
    ├── database.py             # Database connection
    ├── models.py               # SQLAlchemy models
    ├── requirements.txt        # Python dependencies
    ├── Dockerfile              # Container definition
    ├── docker-compose.yml      # Local multi-container setup
    ├── k8s/
    │   ├── deployment.yaml     # K8s deployment (2 replicas)
    │   ├── service.yaml        # LoadBalancer service
    │   ├── ingress.yaml        # Ingress routing
    │   └── postgres.yaml       # Postgres deployment + service
    ├── terraform/
    │   ├── main.tf             # Root module
    │   └── modules/
    │       ├── vpc/            # VPC + subnet module
    │       └── ec2/            # EC2 + security group module
    ├── .github/
    │   └── workflows/
    │       └── ci.yml          # CI pipeline
    └── tests/
        └── test_main.py        # API tests


---

## Run Locally

### Option 1 — Docker only
```bash
docker build -t notes-api .
docker run -p 8000:8000 notes-api
```
Open: localhost:8000/docs

### Option 2 — With Postgres (docker-compose)
```bash
docker-compose up --build
```
Open: localhost:8000/docs

### Option 3 — Kubernetes (local k3d)
```bash
k3d cluster create notecluster --port "8080:80@loadbalancer"
kubectl apply -f k8s/
```
Open: localhost:8080/docs

---

## Deploy to AWS EKS

### 1. Provision infrastructure
```bash
cd terraform
terraform init
terraform apply -auto-approve
```

### 2. Create EKS cluster
```bash
eksctl create cluster \
  --name notes-cluster \
  --region ap-south-1 \
  --node-type t3.small \
  --nodes 2 \
  --managed
```

### 3. Push image to ECR
```bash
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com

docker buildx build --platform linux/amd64 \
  -t <account-id>.dkr.ecr.ap-south-1.amazonaws.com/notes-api:latest \
  --push .
```

### 4. Deploy to cluster
```bash
kubectl apply -f k8s/
```

### 5. Get public URL
```bash
kubectl get services
```

---

## CI/CD Pipeline

GitHub Actions runs on every push to main:
1. Install Python dependencies
2. Run pytest tests
3. Build Docker image
4. Confirm build success

---

## Monitoring

### Local (Prometheus + Grafana)
```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```
Open: localhost:3000 (admin / admin123)

### AWS (CloudWatch)
Metrics automatically collected for all AWS services.
Billing alarm configured to alert on any charges.

---

## Infrastructure as Code (Terraform)

AWS infrastructure provisioned with Terraform:
- VPC with CIDR 10.0.0.0/16
- Public subnet in ap-south-1a
- Security group allowing ports 22 and 8000
- EC2 t2.micro instance (Ubuntu 22.04)
- Remote state stored in S3: notes-app-terraform-state-cherry

Modules:
- modules/vpc — VPC, subnet, availability zone
- modules/ec2 — EC2 instance, security group

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
terraform destroy -auto-approve
```

---

## Security

- Database credentials stored in Kubernetes Secrets
- Never hardcoded in YAML files or pushed to GitHub
- AWS IAM user with least-privilege access
- Security groups restrict access to ports 22 and 8000 only
- Terraform state files excluded from version control

---

## Key Learnings

- Containers solve the "works on my machine" problem
- docker-compose is for development, Kubernetes is for production
- Kubernetes self-heals — deleted pods are automatically replaced
- Terraform makes infrastructure reproducible and version controlled
- Secrets should never live in code or version control
- Monitoring is essential — you can't fix what you can't see
- Mac M1/M2 images need --platform linux/amd64 for AWS deployment

---

