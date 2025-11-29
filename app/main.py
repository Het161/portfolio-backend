from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Het Patel Portfolio API",
    description="Backend API for portfolio website",
    version="1.0.0"
)

# ✅ FIXED: Comprehensive CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://buildbyhet.me",
        "https://www.buildbyhet.me",
        "https://buildbyhet.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# ========== MODELS ==========
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# ========== ROUTES ==========
@app.get("/")
def read_root():
    return {
        "message": "Het Patel Portfolio API",
        "status": "running",
        "version": "1.0.0",
        "frontend": "https://buildbyhet.me"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "portfolio-api"
    }

@app.post("/api/contact")
async def contact_form(form_data: ContactForm, request: Request):
    """
    Handle contact form submissions with comprehensive error handling
    """
    try:
        # Log incoming request
        logger.info(f"📧 Contact form submission from: {form_data.name} ({form_data.email})")
        
        # Get email credentials
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        
        # Validate credentials exist
        if not EMAIL_USER or not EMAIL_PASSWORD:
            logger.error("❌ Email configuration missing")
            raise HTTPException(
                status_code=500,
                detail="Email service not configured"
            )
        
        logger.info(f"✅ Email credentials found for: {EMAIL_USER}")
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        msg['Subject'] = f"Portfolio Contact: {form_data.name}"
        msg['Reply-To'] = form_data.email
        
        # Email body (plain text)
        text_body = f"""
New Contact Form Submission

From: {form_data.name}
Email: {form_data.email}

Message:
{form_data.message}

---
Sent from buildbyhet.me
Reply directly to this email to respond to {form_data.name}
"""
        
        # Email body (HTML)
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">
            New Portfolio Contact
        </h2>
        
        <div style="margin: 20px 0;">
            <p><strong>From:</strong> {form_data.name}</p>
            <p><strong>Email:</strong> <a href="mailto:{form_data.email}">{form_data.email}</a></p>
        </div>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">Message:</h3>
            <p style="white-space: pre-wrap;">{form_data.message}</p>
        </div>
        
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
            <p>Sent from <a href="https://buildbyhet.me">buildbyhet.me</a></p>
            <p>Reply directly to this email to respond to {form_data.name}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach both plain text and HTML
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email with timeout and error handling
        logger.info("📤 Connecting to Gmail SMTP...")
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                server.set_debuglevel(0)  # Disable debug output
                logger.info("🔐 Starting TLS...")
                server.starttls()
                
                logger.info("🔑 Authenticating...")
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                
                logger.info("📨 Sending email...")
                server.send_message(msg)
                
                logger.info("✅ Email sent successfully!")
            
            return {
                "success": True,
                "message": "Email sent successfully",
                "from": form_data.name,
                "to": EMAIL_USER
            }
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP Authentication failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Email authentication failed. Please contact admin."
            )
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send email: {str(e)}"
            )
        except Exception as e:
            logger.error(f"❌ Unexpected error during email send: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Server error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )

# ========== STARTUP EVENT ==========
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Portfolio API started successfully!")
    logger.info(f"📧 Email configured: {bool(os.getenv('EMAIL_USER'))}")
    logger.info(f"🔑 Password configured: {bool(os.getenv('EMAIL_PASSWORD'))}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
