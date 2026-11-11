
#!/bin/bash

set -e

# Preparar directorio compartido de llaves
mkdir -p /shared-ssh
chown -R hadoop:hadoop /shared-ssh

# Crear llave SSH si no existe
if [ ! -f /shared-ssh/id_ed25519 ]; then
    runuser -u hadoop -- ssh-keygen \
        -t ed25519 \
        -N "" \
        -f /shared-ssh/id_ed25519
fi

# Configurar SSH del usuario Hadoop
mkdir -p /home/hadoop/.ssh
chmod 700 /home/hadoop/.ssh

cp /shared-ssh/id_ed25519.pub \
    /home/hadoop/.ssh/authorized_keys

cp /shared-ssh/id_ed25519 \
    /home/hadoop/.ssh/id_ed25519

chmod 600 /home/hadoop/.ssh/authorized_keys
chmod 600 /home/hadoop/.ssh/id_ed25519

chown -R hadoop:hadoop /home/hadoop/.ssh

# Configurar conexión SSH local
cat > /home/hadoop/.ssh/config <<EOF
Host localhost
    HostName localhost
    User hadoop
    IdentityFile /home/hadoop/.ssh/id_ed25519
    StrictHostKeyChecking no
EOF

chown hadoop:hadoop /home/hadoop/.ssh/config
chmod 600 /home/hadoop/.ssh/config

# Iniciar servidor SSH
/usr/sbin/sshd

echo "Hadoop container iniciado correctamente"

# Mantener contenedor activo
exec tail -f /dev/null
