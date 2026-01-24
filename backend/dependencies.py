from fastapi import UploadFile, HTTPException, File
from fastapi.concurrency import run_in_threadpool
from PIL import Image
import magic
import logging

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/bmp',
    'image/tiff'
}

def _validate_and_load_image_sync(file: UploadFile) -> Image.Image:
    """
    Synchronously validate and load an image file.
    Checks size, MIME type, and image integrity.
    """
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size allowed is {MAX_FILE_SIZE // (1024*1024)}MB"
        )

    # Check MIME type
    try:
        file_content = file.file.read(1024)
        file.file.seek(0)

        detected_mime = magic.from_buffer(file_content, mime=True)

        # Simple mapping for common issues where magic might return generic types
        if detected_mime == 'application/octet-stream':
             # Fallback or strict check? Let's be strict but log it.
             pass

        if detected_mime not in ALLOWED_MIME_TYPES:
             raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Only image files are allowed. Detected: {detected_mime}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating file {file.filename}: {e}")
        raise HTTPException(status_code=400, detail="Unable to validate file content.")

    # Load Image
    try:
        image = Image.open(file.file)
        image.load() # Verify integrity
        return image
    except Exception as e:
        logger.error(f"Invalid image content: {e}")
        raise HTTPException(status_code=400, detail="Invalid image content")

async def get_valid_image(image: UploadFile = File(...)) -> Image.Image:
    """
    Dependency to validate and load an uploaded image.
    Returns a PIL Image object.
    """
    return await run_in_threadpool(_validate_and_load_image_sync, image)
