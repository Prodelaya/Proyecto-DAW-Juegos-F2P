#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import time
from urllib.parse import urlparse

import psycopg2


def build_dsn(database_url: str) -> str:
    parsed = urlparse(database_url)
    scheme = parsed.scheme.lower()

    if scheme not in {"postgres", "postgresql"}:
        return ""

    dbname = parsed.path.lstrip("/") or os.getenv("POSTGRES_DB", "postgres")
    host = parsed.hostname or os.getenv("POSTGRES_HOST", "db")
    port = parsed.port or int(os.getenv("POSTGRES_PORT", "5432"))
    user = parsed.username or os.getenv("POSTGRES_USER", "postgres")
    password = parsed.password or os.getenv("POSTGRES_PASSWORD", "postgres")

    return (
        f"dbname={dbname} host={host} port={port} "
        f"user={user} password={password} connect_timeout=3"
    )


def main() -> int:
    command = sys.argv[1:]
    if not command:
        print("[wait_for_postgres] Missing command to execute.", file=sys.stderr, flush=True)
        return 1

    database_url = os.getenv("DATABASE_URL", "")
    dsn = build_dsn(database_url)

    if dsn:
        timeout_seconds = int(os.getenv("WAIT_FOR_DB_TIMEOUT", "60"))
        deadline = time.monotonic() + timeout_seconds

        while True:
            try:
                connection = psycopg2.connect(dsn)
                connection.close()
                print(
                    "[wait_for_postgres] PostgreSQL disponible. Iniciando aplicación...",
                    flush=True,
                )
                break
            except psycopg2.OperationalError as error:
                if time.monotonic() >= deadline:
                    print(
                        "[wait_for_postgres] Timeout esperando PostgreSQL.",
                        file=sys.stderr,
                        flush=True,
                    )
                    print(str(error), file=sys.stderr, flush=True)
                    return 1

                print(
                    "[wait_for_postgres] PostgreSQL todavía no acepta conexiones. Reintentando...",
                    flush=True,
                )
                time.sleep(2)
    else:
        print(
            "[wait_for_postgres] DATABASE_URL no usa PostgreSQL. Se omite la espera explícita.",
            flush=True,
        )

    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
