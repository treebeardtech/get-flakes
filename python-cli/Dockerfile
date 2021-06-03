
FROM python:3.8-slim

# requires poetry build before docker build
COPY dist/deeptest-*whl deeptest-0.0.0-py3-none-any.whl
RUN pip install deeptest-0.0.0-py3-none-any.whl
EXPOSE 8080

CMD gunicorn deeptest.server:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080