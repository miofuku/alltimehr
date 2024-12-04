import re
from typing import Optional
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> Optional[str]:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        str: Normalized email address if valid
        None: If email is invalid
    """
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError:
        return None

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))

def sanitize_input(text: str) -> str:
    """
    Sanitize input text
    
    Args:
        text: Input text to sanitize
    
    Returns:
        str: Sanitized text
    """
    # Remove potentially dangerous characters
    text = re.sub(r'[<>]', '', text)
    # Remove multiple spaces
    text = ' '.join(text.split())
    return text.strip() 