FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY manage.py .
COPY local_pages local_pages
COPY templates templates
COPY example example
RUN mkdir /data && chown 10001:10001 /data
USER 10001:10001

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "local_pages.wsgi"]
