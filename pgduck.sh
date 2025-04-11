#!/bin/bash

DEFAULT_PG_SCHEMA="yh"

# Load and convert PostgreSQL env vars to DuckDB format
source .env
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGUSER="${POSTGRES_USER}"
export PGDATABASE="${POSTGRES_DBNAME}"
export PGHOST="127.0.0.1"
export PGPORT="${POSTGRES_PORT}"

duckdb -cmd "ATTACH '' AS postgres_db (TYPE POSTGRES); USE postgres_db; SET search_path TO '${DEFAULT_PG_SCHEMA}'; $@"