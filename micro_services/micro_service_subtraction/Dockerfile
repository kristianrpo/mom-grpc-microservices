FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=.

EXPOSE 50054

CMD ["sh", "-c", "python -u subtraction_service.py"]


