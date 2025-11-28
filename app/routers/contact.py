# ============================================
# CONTACT ROUTER
# ============================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    message: str
    status: str

@router.post("/", response_model=ContactResponse)
async def send_contact_email(form: ContactForm):
    try:
        EMAIL_USER = os.getenv("EMAIL_USER", "your-email@gmail.com")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
        RECIPIENT_EMAIL = "hetpatelsk@gmail.com"
        
        msg = MIMEMultipart()
        msg['Subject'] = f'Portfolio Contact: {form.name}'
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Reply-To'] = form.email
        
        body = f"""
        New Contact Form Submission
        
        Name: {form.name}
        Email: {form.email}
        
        Message:
        {form.message}
        
        ---
        Sent from Het Patel's Portfolio Website
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return {
            "message": "Thank you! Your message has been sent successfully.",
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send email."
        )
