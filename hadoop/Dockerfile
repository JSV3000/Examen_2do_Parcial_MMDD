FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias, Java 17, Python 3 y OpenSSH Server
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    openssh-server \
    openssh-client \
    wget \
    curl \
    sudo \
    nano \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno de Java y Hadoop (arquitectura amd64)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Descargar e instalar Hadoop 3.3.6 en /opt
RUN cd /opt && \
    wget -q https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzf hadoop-3.3.6.tar.gz && \
    ln -s /opt/hadoop-3.3.6 /opt/hadoop && \
    rm hadoop-3.3.6.tar.gz

# Crear usuario hadoop sin contraseña en texto plano y darle permisos
RUN useradd -m -s /bin/bash hadoop && \
    echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R hadoop:hadoop /opt/hadoop-3.3.6 /opt/hadoop

# Añadir variables al .bashrc de hadoop y a hadoop-env.sh
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /home/hadoop/.bashrc && \
    echo "export HADOOP_HOME=/opt/hadoop" >> /home/hadoop/.bashrc && \
    echo "export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop" >> /home/hadoop/.bashrc && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> /home/hadoop/.bashrc && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

# Configurar llaves SSH sin contraseña para el usuario hadoop
USER hadoop
RUN ssh-keygen -t rsa -P "" -f /home/hadoop/.ssh/id_rsa && \
    cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys && \
    chmod 700 /home/hadoop/.ssh && \
    chmod 600 /home/hadoop/.ssh/authorized_keys && \
    echo "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null" > /home/hadoop/.ssh/config && \
    chmod 600 /home/hadoop/.ssh/config

USER root
RUN mkdir -p /run/sshd /data/input /data/output /ssh_shared && \
    chown -R hadoop:hadoop /data/output /ssh_shared

# Script de arranque: copia la llave privada al volumen compartido para que 'api' pueda entrar por SSH y arranca sshd
CMD cp /home/hadoop/.ssh/id_rsa /ssh_shared/id_rsa && \
    chmod 600 /ssh_shared/id_rsa && \
    echo "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null" > /ssh_shared/config && \
    /usr/sbin/sshd -D