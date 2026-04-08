FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask

EXPOSE 7860

CMD ["python", "inference.py"]