#!/bin/bash
set -x -e
# Database credentials and information
DB_NAME="exampleapp"
DB_USER="exampleuser"
DB_PASSWORD="password"
MIGRATIONS_DIR="$(git rev-parse --show-toplevel)/src/migrations"

# Execute the SQL commands using psql
psql -U postgres -c "CREATE DATABASE $DB_NAME;"
psql -U postgres -c "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"

echo "Database '$DB_NAME' and user '$DB_USER' created with the provided password."

for migration_file in $MIGRATIONS_DIR/*.sql; do
    echo "Executing migration from file: $migration_file"
    psql -U postgres -d exampleapp -f $migration_file
done
