#!/usr/bin/env bash
set -e

if [[ -f .env ]]; then
    source .env
fi

set_db_url() {

    if [[ -z "$DATABASE_URL" ]]; then
        HOST_IP=$(ip addr | grep "inet.*global dynamic" | sed -n 's/.*inet \([0-9.]\+\)\/.*/\1/p')
        echo "DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${HOST_IP}:5432/${POSTGRES_DB}" >> .env
    else
        HOST_IP=$(ip addr | grep "inet.*global dynamic" | sed -n 's/.*inet \([0-9.]\+\)\/.*/\1/p')
        sed -i "s/DATABASE_URL=.*/DATABASE_URL=postgresql:\/\/${POSTGRES_USER}:${POSTGRES_PASSWORD}\@${HOST_IP}:5432\/${POSTGRES_DB}/" .env
    fi
}

update_pg_hba() {

    DOCKER_SUBNET=$(docker network inspect ${COMPOSE_PROJECT_NAME}_net | jq -r '.[0].IPAM.Config[0].Subnet')
    AUTH_METHOD=md5
    PG_HBA_FILE=$(find / -name pg_hba.conf 2> /dev/null | head -n 1)

    if [ -z "$PG_HBA_FILE" ]; then
        echo "pg_hba.conf file not found."
        return 1
    fi

    if grep -q "host\s\+all\s\+all\s\+.*\s\+$AUTH_METHOD" "$PG_HBA_FILE"; then
        echo "Subnet record for docker subnet present in pg_hba.conf. Updating..."
        sed -i "s|^host\s\+all\s\+all\s\+.*\s\+$AUTH_METHOD\$|host\tall\tall\t$DOCKER_SUBNET\t$AUTH_METHOD|" "$PG_HBA_FILE"
        echo "Updated."
        sudo systemctl restart postgresql
    else
        echo "No record found for docker subnet in pg_hba.conf. Adding..."
        echo "host\tall\tall\t$DOCKER_SUBNET\t$AUTH_METHOD" >> "$PG_HBA_FILE"
        echo "Added."
        sudo systemctl restart postgresql
    fi
}

up() {
    set_db_url    
    docker compose up -d
    update_pg_hba
}

down() {
    docker compose down
}

rebuild() {
    down
    docker compose build 
    up
}

usage() {
    echo "Usage: $0 <subcommand>"
    echo "Subcommands:":wq
    echo "  up - spin up the dev environment"
    echo "  down - shutdown the dev environment"
    echo "  rebuild - rebuild the containers and restart the dev environment"
}

if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

case $1 in
    up)
        up
        ;;
    down)
        down
        ;;
    rebuild)
        rebuild
        ;;
    *)
        echo "Unknown subcommand: $1"
        usage
        exit 1
        ;;
esac
