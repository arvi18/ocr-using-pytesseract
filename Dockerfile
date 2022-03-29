FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"
RUN apk add --updatee --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN ls -la
RUN pip install -r requirements.txt
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
