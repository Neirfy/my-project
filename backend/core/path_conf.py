import os

from pathlib import Path

BasePath = Path(__file__).resolve().parent.parent

ALEMBIC_Versions_DIR = os.path.join(BasePath, "migrations", "versions")

STORE_DIR = os.path.join(BasePath, "store")

LOG_DIR = os.path.join(BasePath, "logs")

IP2REGION_XDB = os.path.join(BasePath, "static", "ip2region.xdb")

STATIC_DIR = os.path.join(BasePath, "static")

CERTS_DIR = os.path.join(BasePath, "certs")
