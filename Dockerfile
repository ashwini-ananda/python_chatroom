# FROM python:3

# WORKDIR /chatroom

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY ./app ./app

# CMD ["python", "./app/chat_server.py"]
# CMD ["python", "./app/client.py"]

FROM python:3.7-slim as base

# ---- compile image -----------------------------------------------
FROM base AS compile-image
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  gcc

RUN python -m venv /app/env
ENV PATH="/app/env/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
# pip install is fast here (while slow without the venv) :
RUN pip install -r requirements.txt

# ---- build image -----------------------------------------------
FROM base AS build-image
COPY --from=compile-image /app/env /app/env

# Make sure we use the virtualenv:
ENV PATH="/app/env/bin:$PATH"
COPY . /app
WORKDIR /app
# CMD ["python", "-m unittest test_y.py"]
RUN pip uninstall pyhton3-protobuf
RUN pip install --upgrade pip
RUN pip install --upgrade protobuf
# RUN pytest -v app/test_1.py
