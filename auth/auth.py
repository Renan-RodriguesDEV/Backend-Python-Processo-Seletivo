import os
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Configuração
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET", "my_secret_compartilhado_com_csharp")

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
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # 2. Decodificar e validar o token
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token inválido: {str(e)}"
        )
