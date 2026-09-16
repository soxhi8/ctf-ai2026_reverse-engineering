#!/bin/bash
set -euo pipefail

USER="flag-validator"

[ "$EUID" -eq 0 ] || { echo "Run with root permissions."; exit 1; }

if id "$USER" &>/dev/null; then
    read -p "User $USER already exists. Delete user and start over? [y/N]: " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        USER_UID=$(id -u "$USER")
        loginctl disable-linger "$USER" ||:
        loginctl kill-user "$USER" 2>/dev/null ||:
        pkill -u "$USER_UID" 2>/dev/null ||:
        sleep 0.5
        pkill -9 -u "$USER_UID" 2>/dev/null ||:
        sleep 0.5
        userdel -r "$USER"
        if command -v firewall-cmd &> /dev/null; then
            firewall-cmd --permanent --remove-port=80/tcp
            firewall-cmd --permanent --remove-port=443/tcp
            firewall-cmd --reload
        fi
    else
        echo "Exiting setup."
        exit 1
    fi
fi

# Allow rootless users to bind ports 80 and 443
if grep -q "net.ipv4.ip_unprivileged_port_start" /etc/sysctl.conf 2>/dev/null; then
    sed -i 's/^net.ipv4.ip_unprivileged_port_start.*/net.ipv4.ip_unprivileged_port_start=80/' /etc/sysctl.conf
else
    echo "net.ipv4.ip_unprivileged_port_start=80" >> /etc/sysctl.conf
fi
sysctl -w net.ipv4.ip_unprivileged_port_start=80

useradd -m "$USER"
loginctl enable-linger "$USER"
USER_UID=$(id -u "$USER")

QUADLET_DIR="/home/$USER/.config/containers/systemd"
mkdir -p "$QUADLET_DIR"

cat <<EOF > "$QUADLET_DIR/flag-validator.network"
[Unit]
Description=Network for Flag Validator

[Network]
EOF

cat <<EOF > "$QUADLET_DIR/flag-validator-app.container"
[Unit]
Description=Flag Validator App Container
After=network-online.target

[Container]
Image=localhost/flag_validator-app:latest
Network=flag-validator.network
NetworkAlias=app

[Service]
Restart=always
EOF

cat <<EOF > "$QUADLET_DIR/flag-validator-caddy.container"
[Unit]
Description=Flag Validator Caddy Container
After=network-online.target flag-validator-app.service
Requires=flag-validator-app.service

[Container]
Image=docker.io/library/caddy:2
Network=flag-validator.network
PublishPort=80:80
PublishPort=443:443
Volume=/home/$USER/Caddyfile:/etc/caddy/Caddyfile:Z
Volume=flag-validator-caddy_data:/data
Volume=flag-validator-caddy_config:/config

[Service]
Restart=always
EOF

chown -R "$USER:$USER" "/home/$USER/.config"

# Copy Caddyfile persistently
cp Caddyfile "/home/$USER/Caddyfile"
chown "$USER:$USER" "/home/$USER/Caddyfile"

# Copy build context
mkdir -p "/home/$USER/build"
cp app.py Dockerfile requirements.txt "/home/$USER/build/"
chown -R "$USER:$USER" "/home/$USER/build"

# Build image and cleanup
su - "$USER" -c "podman build -t localhost/flag_validator-app:latest ~/build && rm -rf ~/build"

# Reload and start
su - "$USER" -c "XDG_RUNTIME_DIR=/run/user/$USER_UID systemctl --user daemon-reload"
su - "$USER" -c "XDG_RUNTIME_DIR=/run/user/$USER_UID systemctl --user start flag-validator-caddy.service"

if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=80/tcp
    firewall-cmd --permanent --add-port=443/tcp
    firewall-cmd --reload
fi

echo "Installed user flag-validator and started services on ports 80 and 443."
