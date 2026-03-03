import hashlib
import hmac
import os
from db import fetch_one, execute

# Segredo simples (pra MVP). Em produção, coloque isso como variável de ambiente.
APP_SALT = os.environ.get("APP_SALT", "troque-esse-salt-em-producao")

def hash_password(password: str) -> str:
    # PBKDF2 (ok pra MVP)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        APP_SALT.encode("utf-8"),
        120_000
    )
    return dk.hex()

def verify_password(password: str, password_hash: str) -> bool:
    computed = hash_password(password)
    return hmac.compare_digest(computed, password_hash)

def create_user(username: str, password: str):
    password_hash = hash_password(password)
    execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?);",
        (username.strip().lower(), password_hash)
    )

def authenticate(username: str, password: str) -> bool:
    row = fetch_one(
        "SELECT password_hash FROM users WHERE username = ?;",
        (username.strip().lower(),)
    )
    if not row:
        return False
    return verify_password(password, row["password_hash"])

def user_exists() -> bool:
    row = fetch_one("SELECT COUNT(*) AS c FROM users;")
    return row and row["c"] > 0