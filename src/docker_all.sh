#!/usr/bin/env sh

build() {
    echo "Building and pushing all services..."
    cd ./frontend-service/; make build push
    cd ../user-service/; make build push
    cd ../login-service/; make build push
    cd ../product-service/; make build push
    cd ../order-service/; make build push
}

release() {
    echo "Building and pushing all services..."
    cd ./frontend-service/; make release
    cd ../user-service/; make release
    cd ../login-service/; make release
    cd ../product-service/; make release
    cd ../order-service/; make release
}

usage() {
    echo "Usage: $0 <subcommand>"
    echo "Subcommands:"
    echo "  build - Build and push all services"
    echo "  release - Release all services"
}

# Check for the subcommand
if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

case $1 in
    build)
        build
        ;;
    release)
        release
        ;;
    *)
        echo "Unknown subcommand: $1"
        usage
        exit 1
        ;;
esac

