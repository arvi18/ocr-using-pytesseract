FROM python:3.9-alpine

ENV PATH="/scripts:${PATH}"
RUN apk add --update --no-cache --virtual .tmp gcc g++ libc-dev linux-headers
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2
COPY requirements.txt /requirements.txt
RUN pip install wheel ez_setup setuptools
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /ocr_using_pytesseract
COPY ./ocr_using_pytesseract /ocr_using_pytesseract
WORKDIR /ocr_using_pytesseract
COPY ./scripts /scripts

RUN chomd +x /scripts/*

RUN mkdir  -p /vol/web/media
RUN mkdir  -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chomd -R 755 /vol/web

USER user

CMD ["entrypoint.sh"]
