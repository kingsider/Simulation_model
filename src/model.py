from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelParams:
    sign_prob: dict[str, float]
    num_prob: dict[str, float]
    average_speed: float
    transport_distance: float
    photo_distance: float
    rfid_distance: float
    photo_error: float
    rfid_error: float


@dataclass
class Transit:
    num: str
    photo_detection_time: float
    photo_distance: float
    photo_num: str
    speed: float
    car_model_detected: bool


@dataclass
class RfidDetection:
    rfid_detection_time: float
    rfid_num: Optional[float]
