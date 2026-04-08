FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn streamlit requests

RUN chmod +x start.sh

CMD ["bash", "start.sh"]