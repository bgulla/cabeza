FROM cgr.dev/chainguard/python:latest-dev@sha256:92b8a0af0e138d8f3d169ac3fc92fc691c9f66aa16a6e0fd8d429b645ec349f1 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/vendor -r requirements.txt

FROM cgr.dev/chainguard/python:latest@sha256:231d4a76e8521327dbb3c23094b2c41151501845d2656da3c1a0610981c496c5
WORKDIR /app
COPY --from=builder /app/vendor /app/vendor
COPY app.py .
ENV PYTHONPATH=/app/vendor \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080
EXPOSE 8080
USER 65532:65532
CMD ["/app/app.py"]
