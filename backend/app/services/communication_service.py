from typing import List, Optional
from datetime import datetime, timedelta
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.config import settings
from app.models.application import Application
from app.utils.token import generate_interview_token
import time

class CommunicationService:
    def __init__(self):
        self.smtp_settings = settings.smtp
        self.calendar_creds = settings.google_calendar_creds
        
    async def send_interview_invitation(
        self, 
        candidate_email: str,
        candidate_name: str,
        suggested_times: List[datetime]
    ) -> bool:
        """Send interview invitation email"""
        message = MIMEMultipart()
        message["From"] = self.smtp_settings.username
        message["To"] = candidate_email
        message["Subject"] = "Interview Invitation - Please Confirm Your Interview Time"
        
        # Generate HTML table for time selection
        time_options = "\n".join([
            f"<tr><td><a href='{self._generate_confirmation_link(t)}'>"
            f"{t.strftime('%Y-%m-%d %H:%M')}</a></td></tr>"
            for t in suggested_times
        ])
        
        body = f"""
        <html>
            <body>
                <p>Dear {candidate_name},</p>
                <p>Thank you for your application. We are pleased to inform you that you have passed the initial screening.</p>
                <p>Please select a suitable interview time from the following options:</p>
                <table>{time_options}</table>
                <p>Click on the time to confirm.</p>
                <p>Best regards,<br>HR Team</p>
            </body>
        </html>
        """
        
        message.attach(MIMEText(body, "html"))
        
        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_settings.server,
                port=self.smtp_settings.port,
                use_tls=True
            ) as smtp:
                await smtp.login(
                    self.smtp_settings.username,
                    self.smtp_settings.password
                )
                await smtp.send_message(message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
            
    async def schedule_interview(
        self,
        candidate_email: str,
        interview_time: datetime,
        duration_minutes: int = 60
    ) -> Optional[str]:
        """Schedule interview in Google Calendar"""
        try:
            service = build('calendar', 'v3', credentials=self.calendar_creds)
            
            event = {
                'summary': f'Interview - {candidate_email}',
                'description': 'Video Interview',
                'start': {
                    'dateTime': interview_time.isoformat(),
                    'timeZone': 'Asia/Shanghai',
                },
                'end': {
                    'dateTime': (interview_time + timedelta(minutes=duration_minutes)).isoformat(),
                    'timeZone': 'Asia/Shanghai',
                },
                'attendees': [
                    {'email': candidate_email},
                ],
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"interview-{int(time.time())}",
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                    }
                },
            }
            
            event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            return event.get('id')
        except Exception as e:
            print(f"Failed to schedule interview: {e}")
            return None
            
    def _generate_confirmation_link(self, time: datetime) -> str:
        """Generate confirmation link"""
        token = generate_interview_token(
            email=self.candidate_email,
            interview_time=time
        )
        return f"{settings.base_url}/api/interview/confirm/{token}"