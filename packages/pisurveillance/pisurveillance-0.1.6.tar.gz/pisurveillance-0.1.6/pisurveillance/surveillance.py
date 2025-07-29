import asyncio
import logging
from datetime import datetime
from io import BytesIO
from typing import Optional

import aiohttp
from picamera2 import Picamera2

from pisurveillance.config import env

# Configuration
INFERENCE_URL = f"{env.INFERENCE_BASE_URL}/process"

# Initialize the camera
picam2 = Picamera2()

# Configure the camera
config = picam2.create_preview_configuration()
picam2.configure(config)


def capture_image():
    try:
        # Start the camera
        picam2.start()

        # Capture the image directly as JPEG
        jpeg = BytesIO()
        picam2.capture_file(jpeg, format="jpeg")
        jpeg.seek(0)

        return jpeg
    except Exception as e:
        logging.error(f"Error capturing image: {e}")
        raise e
    finally:
        if picam2:
            picam2.stop()


async def send_image(image: BytesIO):
    # Send to server
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                INFERENCE_URL,
                data={"snapshot": image},
            ) as response:
                if response.status >= 400:
                    message = await response.text()
                    logging.error(f"Inference error {response.status}: {message}")
                data = await response.json()
                return data
    except Exception as e:
        logging.error(f"Error sending image: {e}")


async def start_surveillance(
    capture_frequency: Optional[int] = env.CAPTURE_FREQUENCY,
    device_name: Optional[str] = env.DEVICE_NAME,
    camera_index: Optional[int] = env.CAMERA_INDEX,
):
    try:
        logging.info("👀 Starting surveillance 👀")
        logging.info(f"Device name: {device_name}")
        logging.info(f"Camera index: {camera_index}")
        logging.info(f"Inference server: {INFERENCE_URL}\n\n")
        logging.info("Press Ctrl+C to interrupt\n\n")

        while True:
            logging.info(f"Capturing image at {datetime.now()}")
            image = capture_image()

            logging.info("Sending image for inference...")
            res = await send_image(image)

            logging.info(f"Result: {res}")
            await asyncio.sleep(capture_frequency)

    except asyncio.CancelledError:
        logging.info("🛑 Surveillance cancelled via asyncio.")
    except KeyboardInterrupt:
        logging.info("🛑 Surveillance interrupted by user (Ctrl+C).")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
