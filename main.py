from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from openai import OpenAI
import os
import logging
from typing import Optional
from dotenv import load_dotenv
import docx
from PyPDF2 import PdfReader
import magic
import io

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Text to Speech API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
logger.info(f"Using OpenAI base URL: {OPENAI_BASE_URL}")

# Initialize OpenAI client
try:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    raise

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"  # Default voice
    model: str = "tts-1"  # Default model

class DocumentToSpeechRequest(BaseModel):
    voice: str = "alloy"  # Default voice
    model: str = "tts-1"  # Default model

async def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract text from DOCX file: {str(e)}")

async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        pdf = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF file: {str(e)}")

async def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from a TXT file."""
    try:
        return file_content.decode('utf-8')
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to extract text from TXT file: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    logger.info(f"Received text-to-speech request with voice: {request.voice}, model: {request.model}")
    logger.debug(f"Text content: {request.text[:100]}...")  # Log first 100 chars of text
    
    try:
        logger.debug("Attempting to create speech with OpenAI API")
        response = client.audio.speech.create(
            model=request.model,
            voice=request.voice,
            input=request.text
        )
        logger.info("Successfully generated speech")
        
        return StreamingResponse(
            response.iter_bytes(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="speech.mp3"'
            }
        )
    except Exception as e:
        logger.error(f"Error in text-to-speech endpoint: {str(e)}", exc_info=True)
        error_detail = f"Failed to generate speech: {str(e)}"
        logger.error(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

@app.post("/document-to-speech")
async def document_to_speech(
    file: UploadFile = File(...),
    voice: str = "alloy",
    model: str = "tts-1"
):
    logger.info(f"Received document-to-speech request for file: {file.filename}")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Detect file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_content)
        logger.info(f"Detected file type: {file_type}")
        
        # Extract text based on file type
        if file_type == "application/pdf":
            text = await extract_text_from_pdf(file_content)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = await extract_text_from_docx(file_content)
        elif file_type == "text/plain":
            text = await extract_text_from_txt(file_content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}. Supported types are: PDF, DOCX, and TXT"
            )
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the document")
        
        logger.info(f"Successfully extracted text from document. Length: {len(text)} characters")
        
        # Generate speech from extracted text
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        logger.info("Successfully generated speech from document")
        
        return StreamingResponse(
            response.iter_bytes(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="document_speech.mp3"'
            }
        )
    except Exception as e:
        logger.error(f"Error in document-to-speech endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 