FROM node:23-bookworm-slim AS client-builder

WORKDIR /app/client

RUN corepack enable

COPY client/package.json client/pnpm-lock.yaml client/.npmrc ./
RUN pnpm install --frozen-lockfile

COPY client/ ./
RUN pnpm build


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN python -m pip install --no-cache-dir uv==0.9.17

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY server/ ./server/
COPY --from=client-builder /app/client/build ./client/build

RUN uv run python -m nltk.downloader punkt punkt_tab wordnet

EXPOSE 5000

CMD ["uv", "run", "gunicorn", "--chdir", "server", "app:app", "--bind", "0.0.0.0:5000"]
