FROM python:3.10-slim

WORKDIR /app

# Prevent matplotlib GUI backend issues
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV MPLBACKEND=Agg

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 PRE-BUILD MATPLOTLIB FONT CACHE (CRITICAL FIX)
RUN python - <<EOF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.figure()
plt.close()
EOF

EXPOSE 5000

CMD ["gunicorn", "app:app", "--workers=2", "--threads=2", "--timeout=120", "--preload", "--bind=0.0.0.0:5000"]
