"""
DEPRECATED: This module is no longer used.
Please use local_ml_service.py for local ML model-based detection instead of Hugging Face API.

This file is kept for reference purposes only.
"""
import os
import io
import httpx
import base64
from typing import Union, List, Dict, Any
from PIL import Image
import asyncio
import logging

logger = logging.getLogger(__name__)

# HF_TOKEN is optional for public models but recommended for higher limits
token = os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {token}"} if token else {}
API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
CAPTION_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

async def query_hf_api(image_bytes, labels, client=None):
    """
    Queries Hugging Face API using a shared or new HTTP client.
    """
    if client:
        return await _make_request(client, image_bytes, labels)

    async with httpx.AsyncClient() as new_client:
        return await _make_request(new_client, image_bytes, labels)

async def _make_request(client, image_bytes, labels):
    try:
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        payload = {
            "inputs": image_base64,
            "parameters": {
                "candidate_labels": labels
            }
        }

        try:
            response = await client.post(API_URL, headers=headers, json=payload, timeout=20.0)
            if response.status_code != 200:
                logger.error(f"HF API Error: {response.status_code} - {response.text}")
                return []
            return response.json()
        except Exception as e:
            logger.error(f"HF API Request Exception: {e}")
            return []
    except Exception as e:
        logger.error(f"HF API Request Exception: {e}")
        return []

def _prepare_image_bytes(image: Union[Image.Image, bytes]) -> bytes:
    """
    Helper to get bytes from PIL Image or return bytes as is.
    Avoids unnecessary re-encoding if bytes are already available.
    """
    if isinstance(image, bytes):
        return image

    img_byte_arr = io.BytesIO()
    # If image.format is not available (e.g. newly created image), default to JPEG
    fmt = image.format if image.format else 'JPEG'
    image.save(img_byte_arr, format=fmt)
    return img_byte_arr.getvalue()

async def _detect_clip_generic(image: Union[Image.Image, bytes], labels: List[str], target_labels: List[str], client: httpx.AsyncClient = None):
    try:
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        if not isinstance(results, list):
             return []
        detected = []
        for res in results:
            if isinstance(res, dict) and res.get('label') in target_labels and res.get('score', 0) > 0.4:
                 detected.append({
                     "label": res['label'],
                     "confidence": res['score'],
                     "box": []
                 })
        return detected
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def generate_image_caption(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    """
    Generates a description for the image using Salesforce BLIP model.
    """
    try:
        img_bytes = _prepare_image_bytes(image)

        async def _make_caption_request(c):
             # For image-to-text, usually binary data is sent or JSON with base64 depending on model endpoint type.
             # HF Inference API for image-to-text usually accepts binary image data directly.
             return await c.post(CAPTION_API_URL, headers=headers, content=img_bytes, timeout=30.0)

        if client:
             response = await _make_caption_request(client)
        else:
             async with httpx.AsyncClient() as new_client:
                 response = await _make_caption_request(new_client)

        if response.status_code == 200:
             data = response.json()
             if isinstance(data, list) and len(data) > 0:
                 return data[0].get('generated_text', '')
        else:
             logger.error(f"Caption API Error: {response.status_code} - {response.text}")
        return ""
    except Exception as e:
        logger.error(f"Caption Error: {e}")
        return ""

async def detect_vandalism_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["graffiti", "vandalism", "spray paint", "street art", "clean wall", "public property", "normal street"]
    targets = ["graffiti", "vandalism", "spray paint"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_infrastructure_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["broken streetlight", "damaged traffic sign", "fallen tree", "damaged fence", "pothole", "clean street", "normal infrastructure"]
    targets = ["broken streetlight", "damaged traffic sign", "fallen tree", "damaged fence"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_flooding_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["flooded street", "waterlogging", "blocked drain", "heavy rain", "dry street", "normal road"]
    targets = ["flooded street", "waterlogging", "blocked drain", "heavy rain"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_illegal_parking_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["illegal parking", "wrong parking", "parked on sidewalk", "normal parking"]
    targets = ["illegal parking", "wrong parking", "parked on sidewalk"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_street_light_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["broken streetlight", "street light off", "dark street", "street light on"]
    targets = ["broken streetlight", "street light off"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_fire_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["fire", "smoke", "burning", "normal"]
    targets = ["fire", "smoke", "burning"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_stray_animal_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["stray dog", "stray cow", "animal on road", "normal street"]
    targets = ["stray dog", "stray cow", "animal on road"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_blocked_road_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["blocked road", "road barrier", "construction work", "clear road"]
    targets = ["blocked road", "road barrier"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_tree_hazard_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["fallen tree", "hanging branch", "tree hazard", "normal tree"]
    targets = ["fallen tree", "hanging branch", "tree hazard"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_pest_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["pest infestation", "rats", "mosquito breeding", "clean area"]
    targets = ["pest infestation", "rats", "mosquito breeding"]
    return await _detect_clip_generic(image, labels, targets, client)

async def detect_severity_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["critical", "high severity", "medium severity", "low severity"]
    # This returns just the classification
    try:
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        if isinstance(results, list) and len(results) > 0:
             # Assume sorted by score
             return results[0]
        return {}
    except Exception:
        return {}

async def detect_smart_scan_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    labels = ["pothole", "garbage", "fire", "accident", "normal"]
    try:
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        if isinstance(results, list) and len(results) > 0:
             return results[0]
        return {}
    except Exception:
        return {}
