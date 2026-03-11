FROM python:3.13-alpine3.23
LABEL authors="Yar"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /app

# copy requirements.txt file to work directory
COPY requirements.txt .

# update pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project to work directory
COPY . .

CMD ["uvicorn", "tsub_srv:app", "--host", "0.0.0.0", "--port", "80"]

