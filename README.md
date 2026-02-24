Finance Tracker – Cloud-Native DevOps Project

📌 Overview
Finance Tracker is a cloud-native full-stack application deployed on a production-style Kubernetes environment using GitOps and monitored with a complete observability stack.

This project demonstrates end-to-end DevOps practices including:
Containerization with Docker
Local Kubernetes cluster provisioning using Kind
Kubernetes resource management (Deployments, Services, Ingress, ConfigMaps, Probes)
GitOps-based deployment using ArgoCD
Monitoring with Prometheus
Visualization with Grafana

The goal of this project was to simulate a real-world cloud-native production workflow entirely in a local environment.


🏗 Architecture
Environment Stack
Developer Machine
     ↓
Docker Image Build
     ↓
Kind Cluster (Kubernetes in Docker)
     ↓
Kubernetes Resources (Deployments, Services, Ingress)
     ↓
ArgoCD (GitOps Controller)
     ↓
Prometheus (Metrics Collection)
     ↓
Grafana (Visualization)


🛠 Tech Stack
Application        --> Flask (Python)
Containerization   --> Docker
Cluster            --> Kind
Orchestration      --> Kubernetes
GitOps             --> ArgoCD
Monitoring         --> Prometheus
Visualization      --> Grafana
Package Management --> Helm


⚙️ Project Phases
Phase 1 – Application Containerization

Built Docker image for Flask app
Exposed application on port 5000
Tested locally using Docker

Phase 2 – Kubernetes Deployment (Kind Cluster)

Created local cluster:
kind create cluster --name finance-cluster

Deployed:
Deployment
Service
Ingress
ConfigMap
Liveness & Readiness Probes

Verified:
Pod health
Service connectivity
Ingress routing

Phase 3 – Configuration Management

Externalized environment variables using ConfigMaps
Applied declarative configuration through YAML
Updated application without rebuilding image

Phase 4 – GitOps Implementation (ArgoCD)

Installed ArgoCD in cluster
Connected GitHub repository
Enabled automatic sync
Managed application state declaratively
ArgoCD ensures:
Source of truth = Git
Automatic reconciliation
Drift detection

Phase 5 – Monitoring & Observability

Prometheus
Installed via Helm chart.
Collected:
Pod CPU usage
Memory consumption
Container restarts
Cluster health metrics

Example PromQL query:
rate(container_cpu_usage_seconds_total[5m])

Grafana
Imported Kubernetes dashboards
Configured Prometheus as data source
Set correct panel units (e.g., bytes for memory)
Built custom dashboard for Finance Tracker


🧪 End-to-End Validation (images attached in /images folder)

The system was validated by:
Accessing application via browser
Verifying pod status
Confirming Prometheus target health
bserving live metrics in Grafana
Testing argoCD sync


📂 Repository Structure

example/
├── app.py                     # Flask application entry point
├── Dockerfile                 # Container build definition
├── requirements.txt           # Python dependencies
├── kind-config.yml            # Kind cluster configuration

├── base/                      # Core Kubernetes manifests (Kustomize base)
│   ├── deployment.yml
│   ├── service.yml
│   ├── ingress.yml
│   ├── configmap.yml
│   ├── chart-pvc.yml
│   └── kustomization.yml

├── finance-tracker/           # Helm chart for application
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml
│       ├── service-monitor.yml
│       └── serviceaccount.yaml

├── argocd/                    # GitOps application definitions
│   ├── finance-app.yml
│   ├── monitoring-app.yml
│   └── nodeport.yml

├── monitoring/                # Monitoring Helm configuration
│   ├── Chart.yaml
│   └── values.yml

├── prometheus/                # RBAC configuration for Prometheus
│   ├── cluster-role.yml
│   ├── clusterrole-binding.yml
│   └── prometheus-sa.yml

├── static/                    # Static assets
├── templates/                 # HTML templates
│   ├── index.html
│   └── report.html

├── start.sh                   # Mac/Linux port-forward automation
└── start-ports.ps1            # Windows port-forward automation


📌 Future Improvements
Horizontal Pod Autoscaler (HPA)
Resource requests & limits tuning
CI pipeline integration
TLS configuration for Ingress
Alertmanager integration

