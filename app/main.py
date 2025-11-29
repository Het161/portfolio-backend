from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Het Patel Portfolio API",
    description="Backend API for portfolio website",
    version="1.0.0"
)

# ✅ FIXED: Proper CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",              # Local development
        "https://buildbyhet.me",              # Production domain
        "https://www.buildbyhet.me",          # WWW subdomain
        "https://buildbyhet.vercel.app",      # Vercel domain
        "https://buildbyhet-git-main-het-patels-projects.vercel.app",  # Vercel preview
        "https://*.vercel.app",               # All Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # ✅ Include OPTIONS
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
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
async def contact_form(form_data: ContactForm):
    """
    Handle contact form submissions
    """
    try:
        # Get email credentials from environment variables
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        
        if not EMAIL_USER or not EMAIL_PASSWORD:
            raise HTTPException(
                status_code=500,
                detail="Email configuration not found"
            )
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER  # Send to yourself
        msg['Subject'] = f"Portfolio Contact: {form_data.name}"
        
        # Email body
        body = f"""
        New contact form submission from your portfolio!
        
        Name: {form_data.name}
        Email: {form_data.email}
        
        Message:
        {form_data.message}
        
        ---
        Sent from buildbyhet.me
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return {
            "success": True,
            "message": "Email sent successfully"
        }
        
    except smtplib.SMTPException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )

# ========== STARTUP EVENT ==========
@app.on_event("startup")
async def startup_event():
    print("🚀 Portfolio API started successfully!")
    print(f"📝 API Docs: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
