import os

import jwt
import logging


def get_token_payload(token: str) -> dict:
    try:
        unverified_headers = jwt.get_unverified_header(token)
        return jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=unverified_headers["alg"])

    except Exception as _e:
        logging.error(f'Error JWT decode: {_e}')
        return {}
