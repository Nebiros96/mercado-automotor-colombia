"""Sube assets/logos/ al bucket público brand-logos y actualiza dim_marca.url_logo.

La llave se lee de la variable SUPABASE_SERVICE_ROLE_KEY o de
connections.supabase.service_role en .streamlit/secrets.toml.
La app de Streamlit no la usa en runtime. Solo hace falta para esta carga.
"""

from __future__ import annotations

import json
import os
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

import psycopg2

ROOT = Path(__file__).resolve().parents[1]
LOGOS_DIR = ROOT / "assets" / "logos"
SECRETS = ROOT / ".streamlit" / "secrets.toml"
PROJECT_REF = "mhmyufztulogrljlyyuy"
BUCKET = "brand-logos"
API = f"https://{PROJECT_REF}.supabase.co/storage/v1"
PUBLIC_PREFIX = f"{API}/object/public/{BUCKET}"

CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


def _request(method: str, url: str, key: str, data: bytes | None = None, headers: dict | None = None):
    req_headers = {
        "Authorization": f"Bearer {key}",
        "apikey": key,
    }
    if headers:
        req_headers.update(headers)
    request = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{method} {url} -> {exc.code}: {body}") from exc


def ensure_bucket(key: str) -> None:
    payload = json.dumps({"id": BUCKET, "name": BUCKET, "public": True}).encode()
    try:
        _request(
            "POST",
            f"{API}/bucket",
            key,
            payload,
            {"Content-Type": "application/json"},
        )
    except SystemExit as exc:
        if "already exists" in str(exc).lower() or " 409:" in str(exc):
            return
        raise


def upload_file(key: str, path: Path) -> str:
    content_type = CONTENT_TYPES.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit(f"Extensión no soportada: {path.name}")
    _request(
        "POST",
        f"{API}/object/{BUCKET}/{path.name}",
        key,
        path.read_bytes(),
        {"Content-Type": content_type, "x-upsert": "true"},
    )
    return f"{PUBLIC_PREFIX}/{path.name}"


def update_database(urls_by_slug: dict[str, str]) -> None:
    secrets = tomllib.loads(SECRETS.read_text(encoding="utf-8"))["connections"]["supabase"]
    conn = psycopg2.connect(
        host=secrets["host"],
        port=secrets["port"],
        dbname=secrets["database"],
        user=secrets["username"],
        password=secrets["password"],
        sslmode="require",
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT marca FROM dim_marca ORDER BY marca")
            brands = [row[0] for row in cur.fetchall()]
            for marca in brands:
                slug = _slug(marca)
                url = urls_by_slug.get(slug)
                cur.execute(
                    "UPDATE dim_marca SET url_logo = %s WHERE marca = %s",
                    (url, marca),
                )
                print(f"{marca}: {url or 'sin archivo'}")
    finally:
        conn.close()


def _slug(marca: str) -> str:
    import unicodedata

    ascii_name = unicodedata.normalize("NFKD", marca).encode("ascii", "ignore").decode()
    return ascii_name.lower().replace(" ", "-")


def _service_role_key() -> str:
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if key:
        return key
    if SECRETS.exists():
        secrets = tomllib.loads(SECRETS.read_text(encoding="utf-8"))["connections"]["supabase"]
        key = str(secrets.get("service_role", "")).strip()
    if not key:
        raise SystemExit(
            "Falta la service_role. Agrégala en .streamlit/secrets.toml como "
            "service_role = \"...\" dentro de [connections.supabase], "
            "o expórtala en SUPABASE_SERVICE_ROLE_KEY. "
            "Está en Supabase → Project Settings → API."
        )
    return key


def main() -> None:
    key = _service_role_key()

    files = sorted(
        path for path in LOGOS_DIR.iterdir() if path.suffix.lower() in CONTENT_TYPES
    ) if LOGOS_DIR.exists() else []
    if not files:
        raise SystemExit(f"No hay imágenes en {LOGOS_DIR}")

    ensure_bucket(key)
    urls_by_slug = {}
    for path in files:
        url = upload_file(key, path)
        urls_by_slug[path.stem] = url
        print(f"subido {path.name}")

    update_database(urls_by_slug)
    print(f"{len(urls_by_slug)} logos en {PUBLIC_PREFIX}/")


if __name__ == "__main__":
    main()
