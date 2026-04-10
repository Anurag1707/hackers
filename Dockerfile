FROM python:3.10

WORKDIR /app

COPY . .

# 🔥 ALL REQUIRED DEPENDENCIES
RUN pip install flask openenv-core openai

EXPOSE 7860

# 👉 OpenEnv server run
CMD ["python", "server/app.py"]