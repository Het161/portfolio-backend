# from fastapi import FastAPI, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, EmailStr
# import os
# from dotenv import load_dotenv
# import logging
# import httpx  # For HTTP requests to Resend API

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Create FastAPI app
# app = FastAPI(
#     title="Het Patel Portfolio API",
#     description="Backend API for portfolio website",
#     version="1.0.0"
# )

# # CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://localhost:3001",
#         "https://buildbyhet.me",
#         "https://www.buildbyhet.me",
#         "https://buildbyhet.vercel.app",
#         "https://*.vercel.app",
#     ],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["*"],
#     max_age=3600,
# )

# # Models
# class ContactForm(BaseModel):
#     name: str
#     email: EmailStr
#     message: str

# # Routes
# @app.get("/")
# def read_root():
#     return {
#         "message": "Het Patel Portfolio API",
#         "status": "running",
#         "version": "1.0.0",
#         "frontend": "https://buildbyhet.me"
#     }

# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "service": "portfolio-api"
#     }

# @app.post("/api/contact")
# async def contact_form(form_data: ContactForm, request: Request):
#     """
#     Handle contact form submissions using Resend API
#     """
#     try:
#         logger.info(f"📧 Contact form submission from: {form_data.name} ({form_data.email})")
        
#         # Get Resend API key
#         RESEND_API_KEY = os.getenv("RESEND_API_KEY")
#         TO_EMAIL = os.getenv("TO_EMAIL", "hetpatelsk@gmail.com")
        
#         if not RESEND_API_KEY:
#             logger.error("❌ Resend API key not found")
#             raise HTTPException(
#                 status_code=500,
#                 detail="Email service not configured"
#             )
        
#         logger.info(f"✅ Resend API key found")
#         logger.info(f"📬 Sending to: {TO_EMAIL}")
        
#         # Create email content
#         html_content = f"""
#         <html>
#         <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
#             <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
#                 <h2 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">
#                     New Portfolio Contact
#                 </h2>
                
#                 <div style="margin: 20px 0;">
#                     <p><strong>From:</strong> {form_data.name}</p>
#                     <p><strong>Email:</strong> <a href="mailto:{form_data.email}">{form_data.email}</a></p>
#                 </div>
                
#                 <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
#                     <h3 style="margin-top: 0;">Message:</h3>
#                     <p style="white-space: pre-wrap;">{form_data.message}</p>
#                 </div>
                
#                 <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
#                     <p>Sent from <a href="https://buildbyhet.me">buildbyhet.me</a></p>
#                     <p>Reply directly to this email to respond to {form_data.name}</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         # Send email using Resend API
#         logger.info("📤 Sending email via Resend API...")
        
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 "https://api.resend.com/emails",
#                 headers={
#                     "Authorization": f"Bearer {RESEND_API_KEY}",
#                     "Content-Type": "application/json",
#                 },
#                 json={
#                     "from": "Portfolio <onboarding@resend.dev>",  # Resend's test email
#                     "to": [TO_EMAIL],
#                     "reply_to": form_data.email,
#                     "subject": f"Portfolio Contact: {form_data.name}",
#                     "html": html_content,
#                 },
#                 timeout=10.0,
#             )
        
#         if response.status_code == 200:
#             logger.info("✅ Email sent successfully via Resend!")
#             return {
#                 "success": True,
#                 "message": "Email sent successfully",
#                 "from": form_data.name,
#                 "to": TO_EMAIL
#             }
#         else:
#             logger.error(f"❌ Resend API error: {response.status_code} - {response.text}")
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Failed to send email: {response.text}"
#             )
            
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"❌ Server error: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Server error: {str(e)}"
#         )

# # Startup event
# @app.on_event("startup")
# async def startup_event():
#     logger.info("🚀 Portfolio API started successfully!")
#     logger.info(f"📧 Resend API configured: {bool(os.getenv('RESEND_API_KEY'))}")
#     logger.info(f"📬 Emails will be sent to: {os.getenv('TO_EMAIL', 'hetpatelsk@gmail.com')}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)













from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
import logging
import httpx

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

# CORS Configuration
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

# Models
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str


# ========== BACKGROUND EMAIL FUNCTION ==========
async def send_email_background(name: str, email: str, message: str):
    """
    Send email in the background without blocking the response
    """
    try:
        logger.info(f"📧 Background task: Sending email from {name} ({email})")
        
        RESEND_API_KEY = os.getenv("RESEND_API_KEY")
        TO_EMAIL = os.getenv("TO_EMAIL", "hetpatelsk@gmail.com")
        
        if not RESEND_API_KEY:
            logger.error("❌ Resend API key not found")
            return
        
        # Create email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">
                    New Portfolio Contact
                </h2>
                
                <div style="margin: 20px 0;">
                    <p><strong>From:</strong> {name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                </div>
                
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Message:</h3>
                    <p style="white-space: pre-wrap;">{message}</p>
                </div>
                
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                    <p>Sent from <a href="https://buildbyhet.me">buildbyhet.me</a></p>
                    <p>Reply directly to this email to respond to {name}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email using Resend API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": "Portfolio <onboarding@resend.dev>",
                    "to": [TO_EMAIL],
                    "reply_to": email,
                    "subject": f"Portfolio Contact: {name}",
                    "html": html_content,
                },
                timeout=5.0,  # ✅ Reduced timeout to 5 seconds
            )
        
        if response.status_code == 200:
            logger.info(f"✅ Email sent successfully to {TO_EMAIL}")
        else:
            logger.error(f"❌ Resend API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"❌ Background email error: {str(e)}")


# Routes
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
async def contact_form(form_data: ContactForm, background_tasks: BackgroundTasks):
    """
    Handle contact form submissions - INSTANT RESPONSE with background email
    """
    try:
        logger.info(f"📧 Contact form submission from: {form_data.name} ({form_data.email})")
        
        # ✅ ADD EMAIL TO BACKGROUND TASKS (NON-BLOCKING)
        background_tasks.add_task(
            send_email_background,
            form_data.name,
            form_data.email,
            form_data.message
        )
        
        # ✅ RETURN IMMEDIATELY (USER GETS INSTANT RESPONSE)
        logger.info("✅ Response sent, email queued for background processing")
        return {
            "success": True,
            "message": "Message received! I'll get back to you soon.",
            "from": form_data.name,
        }
            
    except Exception as e:
        logger.error(f"❌ Server error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Portfolio API started successfully!")
    logger.info(f"📧 Resend API configured: {bool(os.getenv('RESEND_API_KEY'))}")
    logger.info(f"📬 Emails will be sent to: {os.getenv('TO_EMAIL', 'hetpatelsk@gmail.com')}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
