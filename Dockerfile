FROM baverman/python38

RUN apk add --no-cache libffi-dev openssl-dev pcre-dev build-base linux-headers

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt
