FROM registry.xiaoyou.host/xiaoyou66/base-poetry:v1.0.1 as builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root

FROM registry.xiaoyou.host/xiaoyou66/base-runtime:v1.0.0 as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /usr/local/lib /usr/local/lib
RUN ldconfig

WORKDIR /app
COPY . /app

CMD ["hypercorn", "-w", "4","-b","0.0.0.0:9000", "main:app"]