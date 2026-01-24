from PIL import Image, ImageFilter
import httpx
from typing import Union
import logging
from backend.hf_api_service import detect_objects_detr

logger = logging.getLogger(__name__)

async def apply_privacy_blur(image: Image.Image, client: httpx.AsyncClient = None) -> Image.Image:
    """
    Detects personal information (persons) in the image and blurs them.
    Returns the modified image.
    """
    try:
        # Detect objects
        detections = await detect_objects_detr(image, client=client)

        if not detections:
            return image

        # Create a copy to modify
        blurred_image = image.copy()
        draw_occurred = False

        for det in detections:
            # Check for 'person' label and high confidence
            # DETR labels are usually lower case
            label = det.get('label', '').lower()
            score = det.get('score', 0)
            box = det.get('box', {})

            if label == 'person' and score > 0.5:
                # Extract coordinates
                # DETR box format: xmin, ymin, xmax, ymax
                xmin = box.get('xmin')
                ymin = box.get('ymin')
                xmax = box.get('xmax')
                ymax = box.get('ymax')

                if xmin is not None and ymin is not None and xmax is not None and ymax is not None:
                    # Ensure bounds
                    width, height = image.size
                    xmin = max(0, int(xmin))
                    ymin = max(0, int(ymin))
                    xmax = min(width, int(xmax))
                    ymax = min(height, int(ymax))

                    # Crop the region
                    region = blurred_image.crop((xmin, ymin, xmax, ymax))

                    # Apply heavy Gaussian Blur
                    # Radius 15 is quite strong, good for privacy
                    blurred_region = region.filter(ImageFilter.GaussianBlur(radius=15))

                    # Paste back
                    blurred_image.paste(blurred_region, (xmin, ymin, xmax, ymax))
                    draw_occurred = True

        if draw_occurred:
            logger.info(f"Privacy protection: Blurred {len([d for d in detections if d.get('label') == 'person'])} detected persons.")

        return blurred_image

    except Exception as e:
        logger.error(f"Error applying privacy blur: {e}")
        # Return original image in case of error to ensure flow continues
        return image
