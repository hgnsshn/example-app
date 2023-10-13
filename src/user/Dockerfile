FROM python:3.11

ARG DATABASE_URL
ARG JWT_SECRET_KEY
ARG USER_SERVICE_PORT

ENV DATABASE_URL=${DATABASE_URL}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["uvicorn"]
CMD ["app:app", "--host", "0.0.0.0", "--port", "${USER_SERVICE_PORT}"]

