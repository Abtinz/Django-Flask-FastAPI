import secrets

def create_secret_key() -> str:
    """Creates a new, secure secret key for signing."""
    return secrets.token_hex(32)