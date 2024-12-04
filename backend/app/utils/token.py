from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from app.config import settings

def generate_interview_token(email: str, interview_time: datetime) -> str:
    """
    Generate interview invitation token
    
    Args:
        email: Candidate email
        interview_time: Interview time
    
    Returns:
        str: JWT token
    
    Raises:
        Exception: If token generation fails
    """
    try:
        payload = {
            "email": email,
            "time": interview_time.isoformat(),
            "type": "interview_confirmation",
            "exp": datetime.utcnow() + timedelta(days=7)  # 7 days validity
        }
        
        return jwt.encode(
            payload,
            settings.secret_key,
            algorithm="HS256"
        )
    except Exception as e:
        raise Exception(f"Failed to generate token: {str(e)}")

def decode_interview_token(token: str) -> dict:
    """
    Decode interview invitation token
    
    Args:
        token: JWT token
    
    Returns:
        dict: Dictionary containing email and interview time
    
    Raises:
        HTTPException: If token is invalid or expired
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token processing error: {str(e)}"
        )