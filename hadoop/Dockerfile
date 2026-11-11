
FROM debian:bookworm-slim

# Evitar preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    openssh-server \
    openssh-client \
    wget \
    curl \
    procps \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PATH="${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"

# Descargar Hadoop 3.3.6
WORKDIR /opt

RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    && tar -xzf hadoop-3.3.6.tar.gz \
    && ln -s /opt/hadoop-3.3.6 /opt/hadoop \
    && rm hadoop-3.3.6.tar.gz

# Crear usuario Hadoop
RUN useradd -m -s /bin/bash hadoop \
    && chown -R hadoop:hadoop /opt/hadoop-3.3.6

# Preparar SSH
RUN mkdir -p /var/run/sshd /shared-ssh \
    && ssh-keygen -A

# Configurar SSH
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config \
    && echo "AllowUsers hadoop" >> /etc/ssh/sshd_config

# Directorios de trabajo
RUN mkdir -p /data/output \
    && chown -R hadoop:hadoop /data/output

# Configurar Hadoop
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

# Copiar script de inicio
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
