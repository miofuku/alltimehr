from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.communication_service import CommunicationService
from app.utils.token import decode_interview_token

router = APIRouter()
comm_service = CommunicationService()

@router.post("/confirm/{interview_token}")
async def confirm_interview(interview_token: str):
    """确认面试时间"""
    try:
        # 解析token获取信息
        interview_info = decode_interview_token(interview_token)
        
        # 在日历中安排面试
        event_id = await comm_service.schedule_interview(
            candidate_email=interview_info["email"],
            interview_time=interview_info["time"]
        )
        
        if not event_id:
            raise HTTPException(
                status_code=500,
                detail="无法安排面试"
            )
            
        return {
            "message": "面试已确认",
            "event_id": event_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 