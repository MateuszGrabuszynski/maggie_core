#!/usr/bin/env bash

ENV_FILE="./.env"

echo "Checking environment variables: MIGRATIONS"

while IFS= read -r line
do
  if [[ $line == "MIGRATIONS=true"* ]]; then
    echo ">>Detected MIGRATIONS equals true"
    python3 manage.py makemigrations
    python3 manage.py migrate
    break
  fi
done < $ENV_FILE