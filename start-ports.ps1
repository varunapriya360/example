# -------------------------------
# Finance Tracker + Monitoring Setup (FIXED)
# -------------------------------

Write-Host "Checking namespaces..."
kubectl get ns

# -------------------------------
# 1️⃣ Finance Tracker App
# -------------------------------
Write-Host "Port-forwarding Finance Tracker app..."
Start-Process powershell -ArgumentList {
    kubectl port-forward svc/finance-tracker -n default 5000:5000
}
Write-Host "Open your app at: http://localhost:5000"

# -------------------------------
# 2️⃣ Argo CD
# -------------------------------
Write-Host "Port-forwarding Argo CD server..."
Start-Process powershell -ArgumentList {
    kubectl port-forward svc/argocd-server -n argocd 8443:443
}
Write-Host "Open Argo CD at: https://localhost:8443"

# -------------------------------
# 3️⃣ Prometheus (FIXED ✅)
# -------------------------------
Write-Host "Port-forwarding Prometheus POD (not service)..."
Start-Process powershell -ArgumentList {
    kubectl port-forward -n monitoring prometheus-monitoring-kube-prometheus-prometheus-0 9090:9090
}
Write-Host "Open Prometheus at: http://localhost:9090"

# -------------------------------
# 4️⃣ Grafana
# -------------------------------
Write-Host "Port-forwarding Grafana..."
Start-Process powershell -ArgumentList {
    kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
}
Write-Host "Open Grafana at: http://localhost:3000"

Write-Host "Grafana Prometheus datasource URL:"
Write-Host "http://localhost:9090"

Write-Host "`nAll port-forwards started!"
