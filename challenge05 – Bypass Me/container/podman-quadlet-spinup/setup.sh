#!/bin/bash
set -euo pipefail

USER="challenge05"
PORT="4842"

[ "$EUID" -eq 0 ] || { echo "Run with root permissions."; exit 1; }

if id "$USER" &>/dev/null; then
    read -p "User $USER already exists. Delete user and start over? [y/N]: " -r
    if [[ $REPLY =~ ^[Yy]$ ]] then
        USER_UID=$(id -u "$USER")
        loginctl disable-linger "$USER" ||:
        loginctl kill-user "$USER" 2>/dev/null ||:
        pkill -u "$USER_UID" 2>/dev/null ||:
        sleep 0.5
        pkill -9 -u "$USER_UID" 2>/dev/null ||:
        sleep 0.5
        userdel -r "$USER"
        if command -v firewall-cmd &> /dev/null; then
            firewall-cmd --permanent --remove-port=$PORT/tcp
            firewall-cmd --reload
        fi
    else
        echo "Exiting setup."
        exit 1
    fi
fi

useradd -m "$USER"

loginctl enable-linger "$USER"

mkdir -p "/home/$USER/.config/containers/systemd"

cp $USER.container "/home/$USER/.config/containers/systemd/"
chown -R "$USER:$USER" "/home/$USER/.config"

cp -r ../docker "/home/$USER/build"
chown -R "$USER:$USER" "/home/$USER/build"
USER_UID=$(id -u "$USER")

machinectl shell "$USER@" /bin/bash -c "
    cd ~/build && 
    podman build -t localhost/$USER:latest . && 
    rm -rf ~/build && 
    systemctl --user daemon-reload && 
    systemctl --user start $USER.service
"

if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=$PORT/tcp
    firewall-cmd --reload
fi

echo "Installed user $USER to run $USER on port $PORT."

