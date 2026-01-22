"""
Hugging Face API Service for VishwaGuru.
Provides zero-shot image classification for various civic issues using OpenAI CLIP model.
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
        return response.json()
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

async def generate_image_caption(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    """
    Generates a description for the image using Salesforce BLIP model.
    """
    try:
        # Note: This implementation was previously using CLIP labels incorrectly.
        # We'll switch to using the Caption API correctly if possible,
        # but for now we'll keep a CLIP fallback or basic description to avoid breaking changes if API is different.

        # Using CLIP as a robust fallback for description generation by checking common scenes
        labels = ["pothole", "garbage pile", "flooded street", "traffic jam", "accident", "fire", "street light", "stray dog", "clean street", "park", "building"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)

        if not isinstance(results, list):
             return "Image analysis unavailable."

        # Find top label
        top_label = "unknown scene"
        top_score = 0
        for res in results:
             if isinstance(res, dict) and res.get('score', 0) > top_score:
                 top_score = res.get('score', 0)
                 top_label = res.get('label')

        return f"Image appears to show {top_label}."
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return "Description generation failed."

async def detect_infrastructure_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["broken streetlight", "damaged traffic sign", "fallen tree", "damaged fence", "pothole", "clean street", "normal infrastructure"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["broken streetlight", "damaged traffic sign", "fallen tree", "damaged fence"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_flooding_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["flooded street", "waterlogging", "blocked drain", "heavy rain", "dry street", "normal road"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["flooded street", "waterlogging", "blocked drain", "heavy rain"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_illegal_parking_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["illegal parking", "car parked on sidewalk", "blocked driveway", "double parking", "legal parking", "empty street"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["illegal parking", "car parked on sidewalk", "blocked driveway", "double parking"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_street_light_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["broken street light", "dark street", "flickering light", "working street light", "daylight"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["broken street light", "dark street", "flickering light"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_fire_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["fire", "smoke", "burning", "clear sky", "normal street"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["fire", "smoke", "burning"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_stray_animal_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["stray dog", "stray cow", "aggressive animal", "animal on road", "pet dog", "no animals"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["stray dog", "stray cow", "aggressive animal", "animal on road"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_blocked_road_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["blocked road", "construction material on road", "fallen tree blocking road", "clear road", "traffic jam"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["blocked road", "construction material on road", "fallen tree blocking road"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_tree_hazard_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["fallen tree", "dangling branch", "tree touching power lines", "healthy tree", "no tree"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["fallen tree", "dangling branch", "tree touching power lines"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_pest_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["mosquito breeding site", "rat infestation", "cockroaches", "clean area", "stagnant water"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)
        return _filter_results(results, ["mosquito breeding site", "rat infestation", "cockroaches", "stagnant water"])
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return []

async def detect_severity_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = ["critical emergency", "high urgency", "medium urgency", "low urgency", "not urgent"]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)

        if not isinstance(results, list):
             return {"level": "Unknown", "confidence": 0, "raw_label": "unknown"}

        top_res = max(results, key=lambda x: x.get('score', 0) if isinstance(x, dict) else 0)
        raw_label = top_res.get('label', 'unknown')
        score = top_res.get('score', 0)

        # Map raw label to level
        level_map = {
            "critical emergency": "Critical",
            "high urgency": "High",
            "medium urgency": "Medium",
            "low urgency": "Low",
            "not urgent": "Low"
        }

        return {
            "level": level_map.get(raw_label, "Medium"),
            "confidence": score,
            "raw_label": raw_label
        }
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return {"level": "Unknown", "confidence": 0, "raw_label": "error"}

async def detect_smart_scan_clip(image: Union[Image.Image, bytes], client: httpx.AsyncClient = None):
    try:
        labels = [
            "pothole", "garbage pile", "flooded street", "fire", "accident",
            "fallen tree", "broken street light", "illegal parking", "graffiti",
            "normal street", "clean road", "building", "park"
        ]
        img_bytes = _prepare_image_bytes(image)
        results = await query_hf_api(img_bytes, labels, client=client)

        if not isinstance(results, list):
             return {"label": "unknown", "score": 0}

        top_res = max(results, key=lambda x: x.get('score', 0) if isinstance(x, dict) else 0)

        # If confidence is low, return unknown
        if top_res.get('score', 0) < 0.3:
             return {"label": "uncertain", "score": top_res.get('score', 0)}

        return {"label": top_res.get('label', 'unknown'), "score": top_res.get('score', 0)}
    except Exception as e:
        logger.error(f"HF Detection Error: {e}")
        return {"label": "error", "score": 0}

def _filter_results(results, target_labels, threshold=0.4):
    if not isinstance(results, list):
            return []

    detected = []
    for res in results:
        if isinstance(res, dict) and res.get('label') in target_labels and res.get('score', 0) > threshold:
                detected.append({
                    "label": res['label'],
                    "confidence": res['score'],
                    "box": [] # CLIP doesn't provide boxes
                })
    return detected
