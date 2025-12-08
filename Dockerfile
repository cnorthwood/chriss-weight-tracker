FROM alpine:3.23

RUN apk --update-cache add python3 poetry

ADD pyproject.toml /app/
ADD poetry.lock /app/
ADD README.md /app/
ADD weight_tracker /app/weight_tracker/

WORKDIR /app
RUN poetry install

ENTRYPOINT ["/usr/bin/poetry", "run", "python3", "-m", "weight_tracker"]
