#!/bin/bash

echo "Checking namespaces..."
kubectl get ns

# -------------------------------
# 1️⃣ Finance Tracker App
# -------------------------------
echo "Port-forwarding Finance Tracker app..."
kubectl port-forward svc/finance-tracker-service -n default 5000:5000 &
echo "Open your app at: http://localhost:5000"

# -------------------------------
# 2️⃣ Argo CD
# -------------------------------
echo "Port-forwarding Argo CD server..."
kubectl port-forward svc/argocd-server -n argocd 8443:443 &
echo "Open Argo CD at: https://localhost:8443"

# -------------------------------
# 3️⃣ Prometheus
# -------------------------------
echo "Port-forwarding Prometheus POD..."
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090 &
echo "Open Prometheus at: http://localhost:9090"

# -------------------------------
# 4️⃣ Grafana
# -------------------------------
echo "Port-forwarding Grafana..."
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80 &
echo "Open Grafana at: http://localhost:3000"

echo ""
echo "All port-forwards started!"