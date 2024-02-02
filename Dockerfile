FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y sshpass openssh-client && \
    rm -rf /var/lib/apt/lists/* && \
    pip install PyYaml \
    simple-term-menu
COPY src /app
CMD ["python" , "Script.py"]