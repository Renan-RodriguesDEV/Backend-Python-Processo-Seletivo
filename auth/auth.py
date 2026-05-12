import os
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.logger import logger

# Configuração
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key-change-this-1234567890")
JWT_ISSUER = os.getenv("JWT_ISSUER", "auth-service")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "reservation-service")

# Esquema de segurança para extrair Bearer token do header
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    """
    Valida o JWT no header Authorization: Bearer <token>

    Args:
        credentials: Extrato do header pelo HTTPBearer

    Returns:
        dict: Payload do token com sub e email

    Raises:
        HTTPException: Se token for inválido, expirado ou ausente
    """

    # 1. Verificar se token existe no header
    logger.debug(f"Received credentials: {credentials}")
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        logger.debug(
            f"Validating token: {credentials.credentials}"
        )  # Log do token recebido
        # 2. Decodificar e validar o token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
        )

        # 3. Verificar se tem os campos obrigatórios
        sub = payload.get("sub")
        email = payload.get("email")

        if not sub or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sem dados obrigatórios (sub, email)",
            )

        return payload  # {"sub": "123", "email": "joao@example.com", ...}

    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token inválido: {str(e)}"
        )
