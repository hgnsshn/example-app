#!/usr/bin/env bash
set -e -x

up() {
    if [[ -f .env ]]; then
        source .env
    fi

    if [[ -z "$DATABASE_URL" ]]; then
        HOST_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n1)
        DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${HOST_IP}:5432/${POSTGRES_DB}"
        echo "DATABASE_URL=${DATABASE_URL}" >> .env
    fi
    docker compose up -d
}

down() {
    docker compose down
}

rebuild() {
    if [[ -f .env ]]; then
        source .env
    fi

    docker compose down
    docker compose build --progress plain --no-cache
    docker compose up -d
}

usage() {
    echo "Usage: $0 <subcommand>"
    echo "Subcommands:"
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
