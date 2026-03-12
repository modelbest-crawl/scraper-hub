FROM python:3.12-slim

WORKDIR /app

COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

COPY packages/ packages/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

ARG OWNER
ARG PROJECT

COPY projects/${OWNER}/${PROJECT}/ projects/${OWNER}/${PROJECT}/
RUN if [ -f projects/${OWNER}/${PROJECT}/requirements.txt ]; then \
      pip install --no-cache-dir -r projects/${OWNER}/${PROJECT}/requirements.txt; \
    fi

ENV SCRAPER_OWNER=${OWNER} \
    SCRAPER_PROJECT=${PROJECT} \
    PYTHONUNBUFFERED=1

CMD python -m projects.${SCRAPER_OWNER}.${SCRAPER_PROJECT}.scraper
