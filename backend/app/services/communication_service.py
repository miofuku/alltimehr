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
        """发送面试邀请邮件"""
        message = MIMEMultipart()
        message["From"] = self.smtp_settings.username
        message["To"] = candidate_email
        message["Subject"] = "面试邀请 - 请确认您的面试时间"
        
        # 生成时间选择的HTML表格
        time_options = "\n".join([
            f"<tr><td><a href='{self._generate_confirmation_link(t)}'>"
            f"{t.strftime('%Y-%m-%d %H:%M')}</a></td></tr>"
            for t in suggested_times
        ])
        
        body = f"""
        <html>
            <body>
                <p>尊敬的 {candidate_name}：</p>
                <p>感谢您的申请。我们很高兴地通知您已通过初步筛选。</p>
                <p>请从以下时间段中选择一个适合您的面试时间：</p>
                <table>{time_options}</table>
                <p>点击时间即可确认。</p>
                <p>祝好，<br>HR团队</p>
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
            print(f"发送邮件失败: {e}")
            return False
            
    async def schedule_interview(
        self,
        candidate_email: str,
        interview_time: datetime,
        duration_minutes: int = 60
    ) -> Optional[str]:
        """在Google Calendar中安排面试"""
        try:
            service = build('calendar', 'v3', credentials=self.calendar_creds)
            
            event = {
                'summary': f'面试 - {candidate_email}',
                'description': '视频面试',
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
            print(f"安排面试失败: {e}")
            return None
            
    def _generate_confirmation_link(self, time: datetime) -> str:
        """生成确认链接"""
        token = generate_interview_token(
            email=self.candidate_email,
            interview_time=time
        )
        return f"{settings.base_url}/api/interview/confirm/{token}"