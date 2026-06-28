FROM python:3.15.0b1-alpine3.23

RUN apk add --no-cache socat

RUN mkdir -p /home/ctf
WORKDIR /home/ctf

RUN echo "picoCTF{70637h3r_f0r3v3r_a5202532}" > flag.txt

COPY lyric-reader.py .

EXPOSE 4859

CMD ["socat", "TCP6-LISTEN:4859,ipv6only=0,reuseaddr,fork", "EXEC:python3 lyric-reader.py,pty,stderr,echo=0"]
