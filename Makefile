IMAGE     ?= cabeza/headers-demo:1.0.0
PORT      ?= 8080
CONTAINER  = cabeza-headers-demo

.PHONY: build run stop logs clean test dev

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -d --name $(CONTAINER) -p $(PORT):8080 $(IMAGE)
	@echo "Listening on http://localhost:$(PORT)"

stop:
	docker stop $(CONTAINER) 2>/dev/null || true

logs:
	docker logs -f $(CONTAINER)

clean: stop
	docker rmi $(IMAGE) 2>/dev/null || true

test:
	python3 -m unittest discover -s tests -v

dev:
	PORT=$(PORT) python3 app.py
