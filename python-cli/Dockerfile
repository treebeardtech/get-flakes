
FROM python:3.8-slim

# requires poetry build before docker build
COPY dist/get-flakes-*whl get-flakes-0.0.0-py3-none-any.whl
RUN pip install get-flakes-0.0.0-py3-none-any.whl
EXPOSE 8080

CMD gunicorn get-flakes.server:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080