FROM ubuntu:20.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root && echo "picoCTF{d3bugg3r_p0w3r_is_4w3s0m3_676d6e5f}" > /root/flag.txt

RUN mkdir -p /home/ctf
WORKDIR /home/ctf

COPY bypassme.bin .
RUN chmod +x bypassme.bin

EXPOSE 4859

CMD ["socat", "TCP-LISTEN:4859,reuseaddr,fork", "EXEC:./bypassme.bin,pty,stderr,echo=0"]
