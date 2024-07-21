FROM python:3.12-alpine
WORKDIR /usr/src/app

# Install dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV MODULE_NAME=main
ENV VARIABLE_NAME=app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]