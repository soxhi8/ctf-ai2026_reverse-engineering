FROM python:3.15.0b1-alpine3.23

RUN apk add --no-cache socat

WORKDIR /app

COPY quiz.py .
RUN echo "picoCTF{my_bIn@4y_3xpl0it_fL@g_58c7b379}" > flag.txt

EXPOSE 4859

CMD ["socat", "TCP-LISTEN:4859,reuseaddr,fork", "EXEC:python3 -u quiz.py,pty,echo=0,stderr"]
