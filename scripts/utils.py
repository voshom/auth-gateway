# utils.py

import json
import base64
import hashlib
import hmac
import os
import time
import logging

from auth_gateway.config import Config

logger = logging.getLogger(__name__)

class JwtHelper:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def encode(self, payload: dict) -> str:
        payload = json.dumps(payload, default=str).encode('utf-8')
        signature = hmac.new(self.secret_key.encode('utf-8'), payload, hashlib.sha256).digest()
        encoded_jwt = base64.urlsafe_b64encode(
            f"{json.dumps(payload).encode('utf-8')}.{signature.hex()}".encode('utf-8')).decode('utf-8')
        return encoded_jwt

    def decode(self, token: str) -> dict:
        try:
            payload_signature = token.split('.')
            if len(payload_signature) != 2:
                logger.error('Invalid token format')
                raise ValueError('Invalid token format')
            payload = json.loads(base64.urlsafe_b64decode(payload_signature[0]))
            signature = base64.urlsafe_b64decode(payload_signature[1])
            expected_signature = hmac.new(self.secret_key.encode('utf-8'), json.dumps(payload, default=str).encode('utf-8'), hashlib.sha256).digest()
            if signature != expected_signature:
                logger.error('Invalid signature')
                raise ValueError('Invalid signature')
            return payload
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f'Failed to decode token: {e}')
            raise ValueError('Invalid token')

class TokenHelper:
    def __init__(self):
        self._secret_key = os.environ.get('SECRET_KEY')
        if not self._secret_key:
            raise RuntimeError('SECRET_KEY environment variable not set')

    def generate(self, user_id: str, expiration_time: int) -> str:
        payload = {
            'user_id': user_id,
            'exp': int(time.time()) + expiration_time
        }
        jwt_helper = JwtHelper(self._secret_key)
        return jwt_helper.encode(payload)

    def verify(self, token: str) -> str:
        jwt_helper = JwtHelper(self._secret_key)
        try:
            payload = jwt_helper.decode(token)
            return payload['user_id']
        except (ValueError, KeyError) as e:
            logger.error(f'Failed to verify token: {e}')
            raise ValueError('Invalid token')