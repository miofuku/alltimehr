from fastapi import APIRouter, HTTPException
from app.services.communication_service import CommunicationService
from app.utils.token import decode_interview_token

router = APIRouter()
comm_service = CommunicationService()

@router.post("/confirm/{interview_token}")
async def confirm_interview(interview_token: str):
    """Confirm interview time and schedule in calendar"""
    try:
        # Decode and validate token
        interview_info = decode_interview_token(interview_token)
        
        # Schedule interview with video meeting
        event_id = await comm_service.schedule_interview(
            candidate_email=interview_info["email"],
            interview_time=interview_info["time"]
        )
        
        if not event_id:
            raise HTTPException(
                status_code=500,
                detail="Failed to schedule interview"
            )
            
        return {
            "status": "success",
            "message": "Interview scheduled successfully",
            "event_id": event_id,
            "time": interview_info["time"].isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 