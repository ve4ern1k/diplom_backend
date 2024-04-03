import jwt
from datetime import datetime
from database import User


SECRET_TOKEN = 'sn6joCksX8xjtK18BB84GSgsLXF8sVhBiP1e7'


def generate_token(user: User):
    return jwt.encode(
        {
            'user_id': user.id,
            'created': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        },
        SECRET_TOKEN, 
        algorithm="HS256"
    )


def decode_token(token: str):
    return jwt.decode(token, SECRET_TOKEN, algorithms=['HS256'])
