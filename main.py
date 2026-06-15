"""
Medici - Autonomous WhatsApp Medical Store Agent
FastAPI Server with WhatsApp Cloud API Webhook
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/medici.log", rotation="10 MB", level="INFO")
logger.info("Medici server starting...")

# Initialize FastAPI app
app = FastAPI(
    title="Medici - WhatsApp Medical Store Agent",
    description="Autonomous WhatsApp agent for medical store inventory",
    version="1.0.0"
)

# Constants
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "YOUR_VERIFY_TOKEN")
BOSS_FATHER_PHONE = os.getenv("BOSS_FATHER_PHONE", "YOUR_FATHER_NUMBER")

# In-memory storage (will be populated in later phases)
inventory_text: Optional[str] = None
skill_md: Optional[str] = None


# ============================================================================
# Health Check
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "service": "medici"}


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "inventory_loaded": inventory_text is not None,
        "skill_loaded": skill_md is not None
    }


# ============================================================================
# WhatsApp Cloud API Webhook Endpoints
# ============================================================================

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    WhatsApp Cloud API verification endpoint.
    Meta sends a GET request with hub.verify_token to verify the webhook.
    """
    hub_mode = request.query_params.get("hub.mode")
    hub_token = request.query_params.get("hub.verify_token")
    hub_challenge = request.query_params.get("hub.challenge")

    logger.info(f"Webhook verification request: mode={hub_mode}, token={hub_token}")

    if hub_mode == "subscribe" and hub_token == WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully!")
        return hub_challenge
    else:
        logger.warning(f"Webhook verification failed! Expected token: {WHATSAPP_VERIFY_TOKEN}")
        raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    WhatsApp Cloud API webhook endpoint.
    Receives both text and image messages from WhatsApp.
    """
    try:
        body = await request.json()
        logger.info(f"Received webhook: {json.dumps(body, indent=2)}")

        # Extract entry data
        entries = body.get("entry", [])
        if not entries:
            return JSONResponse({"status": "ok", "message": "No entries"})

        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    await process_message(message)

        return JSONResponse({"status": "ok"})

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


async def process_message(message: Dict[str, Any]):
    """
    Process incoming WhatsApp message.
    Routes to text or image handler based on message type.
    """
    message_type = message.get("type")
    from_number = message.get("from")

    logger.info(f"Processing {message_type} from {from_number}")

    if message_type == "text":
        await handle_text_message(message)
    elif message_type == "image":
        await handle_image_message(message)
    else:
        logger.warning(f"Unsupported message type: {message_type}")


async def handle_text_message(message: Dict[str, Any]):
    """Handle incoming text message"""
    text = message.get("text", {}).get("body", "")
    from_number = message.get("from")

    logger.info(f"Text message from {from_number}: {text}")

    # TODO: Route to DeepSeek for processing
    # For now, return a placeholder response
    await send_whatsapp_message(
        to=from_number,
        text="Namaste! This is Medici, your medical store assistant. How can I help you today?"
    )


async def handle_image_message(message: Dict[str, Any]):
    """Handle incoming image message (prescription)"""
    image_id = message.get("image", {}).get("id")
    from_number = message.get("from")

    logger.info(f"Image message from {from_number}, image_id: {image_id}")

    # TODO: Download image and route to Gemma Vision OCR
    await send_whatsapp_message(
        to=from_number,
        text="Received your prescription image! Processing... (OCR not yet implemented)"
    )


async def send_whatsapp_message(to: str, text: str):
    """
    Send message via WhatsApp Cloud API.
    TODO: Implement with actual WhatsApp Business API call.
    """
    logger.info(f"Sending to {to}: {text}")
    # Placeholder - will implement in later phase when WhatsApp gateway details provided


# ============================================================================
# Phase 2: PDF Inventory Loader (Stub)
# ============================================================================

def load_inventory_pdf(pdf_path: str = "inventory.pdf") -> str:
    """
    Parse inventory PDF into text.
    Will be implemented in Phase 2.
    """
    global inventory_text
    logger.info(f"Loading inventory from {pdf_path}...")

    # Placeholder - will implement with PyPDF2
    inventory_text = "[PDF inventory will be loaded here]"
    logger.info("Inventory loaded (placeholder)")
    return inventory_text


# ============================================================================
# Phase 3: Skill.md Loader (Stub)
# ============================================================================

def load_skill_md() -> str:
    """
    Load the skill.md file for agent behavior.
    Will be implemented in Phase 3.
    """
    global skill_md
    skill_path = Path("skill.md")

    if skill_path.exists():
        skill_md = skill_path.read_text(encoding="utf-8")
        logger.info("skill.md loaded successfully")
    else:
        skill_md = "# CORE IDENTITY\nYou are Medici, the autonomous medical store agent."
        logger.warning("skill.md not found, using default")

    return skill_md


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on server startup"""
    logger.info("=" * 50)
    logger.info("Medici Server Starting Up")
    logger.info("=" * 50)

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Load inventory (Phase 2 stub)
    load_inventory_pdf()

    # Load skill.md (Phase 3 stub)
    load_skill_md()

    logger.info("Startup complete!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
