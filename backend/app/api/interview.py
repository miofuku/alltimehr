from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.communication_service import CommunicationService
from app.utils.token import decode_interview_token

router = APIRouter()
comm_service = CommunicationService()

@router.post("/confirm/{interview_token}")
async def confirm_interview(interview_token: str):
    """Confirm interview time"""
    try:
        # Parse token to get information
        interview_info = decode_interview_token(interview_token)
        
        # Schedule interview in calendar
        event_id = await comm_service.schedule_interview(
            candidate_email=interview_info["email"],
            interview_time=interview_info["time"]
        )
        
        if not event_id:
            raise HTTPException(
                status_code=500,
                detail="Unable to schedule interview"
            )
            
        return {
            "message": "Interview confirmed",
            "event_id": event_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 