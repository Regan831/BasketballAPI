FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY model.pkl ./
COPY main.py ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]