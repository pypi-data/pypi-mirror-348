import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    INFERENCE_BASE_URL: str = os.getenv("INFERENCE_BASE_URL", "http://raspberrypi.local:8000")
    DEVICE_NAME: str = os.getenv("DEVICE_NAME", "main_camera")
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", "0"))
    CAPTURE_FREQUENCY: int = int(os.getenv("CAPTURE_FREQUENCY", "10"))


env = Config()
