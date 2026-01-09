"""
File upload validation utility for VishwaGuru backend.
Provides security checks for uploaded files including size limits, 
MIME type validation, and content verification.
"""
from fastapi import UploadFile, HTTPException
import magic
import os
import urllib.parse
import unicodedata
from typing import Set, Optional

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
ALLOWED_IMAGE_MIME_TYPES: Set[str] = {
    'image/jpeg',
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
    '.tiff'
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
                detail="Invalid file type. Please upload a valid image file."
            )
    else:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    # Check file size and read content efficiently
    # Try to get size from file object first, otherwise read in chunks
    file_content = b''
    file_size = 0
    
    try:
        # Some UploadFile implementations have a size attribute
        if hasattr(file, 'size') and file.size is not None:
            file_size = file.size
            # Check size before reading
            if file_size == 0:
                raise HTTPException(status_code=400, detail="Empty file not allowed")
            if file_size > max_size:
                raise HTTPException(status_code=400, detail="File too large")
            # Now safe to read the full content
            file_content = await file.read()
        else:
            # Read file in chunks to check size and accumulate content
            chunk_size = 8192  # 8KB chunks
            chunks = []
            total_size = 0
            
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
                total_size += len(chunk)
                # Stop reading if we exceed max size
                if total_size > max_size:
                    raise HTTPException(status_code=400, detail="File too large")
            
            file_size = total_size
            file_content = b''.join(chunks)
            
            # Validate size
            if file_size == 0:
                raise HTTPException(status_code=400, detail="Empty file not allowed")
                
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to process file")
    
    # Validate MIME type using python-magic (content-based detection)
    try:
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in allowed_mime_types:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )
    except HTTPException:
        # Re-raise HTTPException from the mime type check
        raise
    except Exception:
        # If magic fails for any reason, reject the file for safety
        # Don't expose internal error details to prevent information leakage
        raise HTTPException(
            status_code=400,
            detail="Unable to verify file type"
        )
    
    # Reset file pointer to beginning for subsequent reads
    await file.seek(0)


def validate_filename(filename: str) -> str:
    """
    Sanitize and validate filename to prevent path traversal attacks.
    Uses multiple layers of defense including pattern checks and normalization.
    
    Args:
        filename: Original filename from upload
        
    Returns:
        Sanitized filename safe for filesystem operations
        
    Raises:
        HTTPException: If filename contains invalid characters or suspicious patterns
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    # First, URL decode to catch encoded path traversal attempts like %2e%2e
    try:
        decoded_filename = urllib.parse.unquote(filename)
    except Exception:
        decoded_filename = filename
    
    # Check for suspicious patterns in both original and decoded versions
    suspicious_patterns = ['..', '/', '\\', '\x00']
    for pattern in suspicious_patterns:
        if pattern in filename or pattern in decoded_filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Additional check for Unicode normalization bypasses
    try:
        normalized = unicodedata.normalize('NFKC', decoded_filename)
        for pattern in suspicious_patterns:
            if pattern in normalized:
                raise HTTPException(status_code=400, detail="Invalid filename")
    except Exception:
        # If normalization fails, reject the filename
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Remove any path components (belt and suspenders approach)
    filename = os.path.basename(normalized)
    
    # Remove all control characters (ASCII and Unicode)
    # Filter out characters that are control characters or format characters
    sanitized = []
    for char in filename:
        cat = unicodedata.category(char)
        # Keep printable characters, exclude control (Cc), format (Cf), surrogate (Cs), and unassigned (Cn)
        if cat not in ('Cc', 'Cf', 'Cs', 'Cn', 'Co'):
            sanitized.append(char)
    filename = ''.join(sanitized)
    
    # Validate final filename
    if not filename or len(filename) > 255:
        raise HTTPException(status_code=400, detail="Invalid filename after sanitization")
    
    return filename
