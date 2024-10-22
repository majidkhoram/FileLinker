FROM ubuntu:22.04 AS builder
WORKDIR /app
COPY . /srv/
RUN apt update && \
    apt install --yes --no-install-suggests --no-install-recommends curl nginx python3-pip python3-venv gcc libpython3-dev && \
    python3 -m venv /app && \
    /app/bin/pip install --upgrade pip setuptools wheel && \
    /app/bin/pip install --disable-pip-version-check -r requirments.txt

# build into a distroless image
FROM gcr.io/distroless/python3-debian12
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY --from=builder /usr/local/bin/python /usr/local/bin/python
COPY --from=builder /usr/local/bin/python3 /usr/local/bin/python3
COPY --from=builder /app /app
WORKDIR /app
ENTRYPOINT ["/app/bin/python", "-u", "FileLinker.py"]