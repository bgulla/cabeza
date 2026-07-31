# cabeza

[![Build](https://github.com/bgulla/cabeza/actions/workflows/docker.yml/badge.svg)](https://github.com/bgulla/cabeza/actions/workflows/docker.yml)
[![Image](https://ghcr-badge.egpl.dev/bgulla/cabeza/latest_tag?trim=major&label=ghcr&color=%2300ff41)](https://github.com/bgulla/cabeza/pkgs/container/cabeza)
[![Image Size](https://ghcr-badge.egpl.dev/bgulla/cabeza/size?color=%2300ff41)](https://github.com/bgulla/cabeza/pkgs/container/cabeza)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

Dumps every HTTP header and request detail that reaches it. Useful for inspecting what a Kubernetes ingress, load balancer, or reverse proxy actually forwards.

```
$ curl http://your-ingress-host/
```

```
CABEZA REQUEST DUMP
===================
METHOD: GET
PATH: /
REMOTE_ADDR: 10.0.0.1
SCHEME: http
HOST: your-ingress-host

HEADERS:
-------
Accept: */*
Host: your-ingress-host
X-Forwarded-For: 1.2.3.4
X-Forwarded-Proto: https
X-Real-Ip: 1.2.3.4
...
```

## Usage

```bash
make build    # build the image
make run      # start on localhost:8080 (detached)
make logs     # follow logs
make stop     # stop the container
make dev      # run locally without Docker (requires Flask installed)
make clean    # stop + remove the image
make test     # run unit tests
```

Override defaults:

```bash
make run PORT=9090
make build IMAGE=registry.example.com/cabeza:v1.2.0
```

All paths and HTTP methods are handled — hit `/foo/bar`, POST, PUT, whatever.

## Deploy to Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cabeza
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cabeza
  template:
    metadata:
      labels:
        app: cabeza
    spec:
      containers:
        - name: cabeza
          image: cabeza/headers-demo:1.0.0
          ports:
            - containerPort: 8080
          securityContext:
            runAsNonRoot: true
            runAsUser: 65532
            allowPrivilegeEscalation: false
---
apiVersion: v1
kind: Service
metadata:
  name: cabeza
spec:
  selector:
    app: cabeza
  ports:
    - port: 80
      targetPort: 8080
```

Point your ingress at the `cabeza` service, then hit it from a browser or curl to see exactly what headers land at the pod.

## Details

- Base image: [Chainguard Python](https://images.chainguard.dev/directory/image/python/overview), pinned by digest — no root, no shell, minimal attack surface
- Multi-stage build: pip runs in the `-dev` stage; the final image is distroless
- Runs as UID 65532 (Chainguard's standard `nonroot` user)
- Responds to any path and any HTTP method
