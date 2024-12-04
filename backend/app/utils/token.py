from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from app.config import settings

def generate_interview_token(email: str, interview_time: datetime) -> str:
    """
    生成面试邀请令牌
    
    Args:
        email: 候选人邮箱
        interview_time: 面试时间
    
    Returns:
        str: JWT令牌
    """
    payload = {
        "email": email,
        "time": interview_time.isoformat(),
        "type": "interview_confirmation",
        "exp": datetime.utcnow() + timedelta(days=7)  # 7天有效期
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm="HS256"
    )

def decode_interview_token(token: str) -> dict:
    """
    解码面试邀请令牌
    
    Args:
        token: JWT令牌
    
    Returns:
        dict: 包含邮箱和面试时间的字典
    
    Raises:
        jwt.InvalidTokenError: 令牌无效
        jwt.ExpiredSignatureError: 令牌过期
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"]
        )
        
        if payload["type"] != "interview_confirmation":
            raise jwt.InvalidTokenError("Invalid token type")
            
        return {
            "email": payload["email"],
            "time": datetime.fromisoformat(payload["time"])
        }
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        ) from e 