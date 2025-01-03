FROM python:3.13-slim
WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
EXPOSE 8000
ENV MODULE_NAME=main
ENV VARIABLE_NAME=app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]