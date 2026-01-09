"""
File upload validation utility for VishwaGuru backend.
Provides security checks for uploaded files including size limits, 
MIME type validation, and content verification.
"""
from fastapi import UploadFile, HTTPException
import magic
import os
from typing import Set, Optional

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
ALLOWED_IMAGE_MIME_TYPES: Set[str] = {
    'image/jpeg',
    'image/jpg', 
    'image/png',
    'image/gif',
    'image/webp',
    'image/bmp',
    'image/tiff'
}

ALLOWED_IMAGE_EXTENSIONS: Set[str] = {
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.webp',
    '.bmp',
    '.tiff',
    '.tif'
}


async def validate_image_upload(
    file: UploadFile,
    max_size: int = MAX_FILE_SIZE,
    allowed_mime_types: Optional[Set[str]] = None,
    allowed_extensions: Optional[Set[str]] = None
) -> None:
    """
    Validate an uploaded image file for security and format requirements.
    
    Args:
        file: The uploaded file from FastAPI
        max_size: Maximum allowed file size in bytes (default: 10MB)
        allowed_mime_types: Set of allowed MIME types (default: common image types)
        allowed_extensions: Set of allowed file extensions (default: common image extensions)
        
    Raises:
        HTTPException: If validation fails with appropriate status code and detail message
    """
    if allowed_mime_types is None:
        allowed_mime_types = ALLOWED_IMAGE_MIME_TYPES
    
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_IMAGE_EXTENSIONS
    
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file extension
    if file.filename:
        _, ext = os.path.splitext(file.filename.lower())
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension. Allowed extensions: {', '.join(allowed_extensions)}"
            )
    else:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    # Read file content for validation
    file_content = await file.read()
    file_size = len(file_content)
    
    # Validate file size
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")
    
    if file_size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB"
        )
    
    # Validate MIME type using python-magic (content-based detection)
    try:
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in allowed_mime_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_mime_types)}"
            )
    except Exception as e:
        # If magic fails, reject the file for safety
        raise HTTPException(
            status_code=400,
            detail=f"Unable to verify file type: {str(e)}"
        )
    
    # Reset file pointer to beginning for subsequent reads
    await file.seek(0)


def validate_filename(filename: str) -> str:
    """
    Sanitize and validate filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename from upload
        
    Returns:
        Sanitized filename safe for filesystem operations
        
    Raises:
        HTTPException: If filename contains invalid characters
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Check for suspicious patterns
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Remove any null bytes
    filename = filename.replace('\x00', '')
    
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid filename after sanitization")
    
    return filename
