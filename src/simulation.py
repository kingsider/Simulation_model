from enum import Enum
from typing import List, Tuple, Optional

from src.generator import generate_plate, generate_transit
from src.model import Transit, ModelParams, RfidDetection
from heapq import heappush, heappop

import numpy as np


class _Event(Enum):
    PHOTO_TRANSIT = 0
    RFID_DETECTION = 1
    START_MERGE = 2


_EventQueue = List[Tuple[float, _Event, Optional[int]]]
_Transits = List[Tuple[int, Transit]]
_RfidDetections = List[Tuple[int, RfidDetection]]


def simulate(
        sign_prob: dict[str, float],
        num_prob: dict[str, float],
        transport_distance: float,
        photo_distance: [float, float],
        rfid_distance: [float, float],
        speed: list[float, float],
        distance_between_transports: float,
        photo_error: float,
        rfid_error: float,
        car_error: float,
        num_transits=100_000
):
    assert 0 <= car_error <= 1
    assert 0 <= rfid_error <= 1
    assert 0 <= photo_error <= 1

    cur_time = 0
    cur_transits = 0

    _queue: _EventQueue = []  # use heappush and heappop
    transits: _Transits = []
    rfid_detections: _RfidDetections = []

    # init model

    __push_photo_event(
        _queue=_queue,
        cur_time=cur_time,
        speed=speed,
        distance_between_transports=distance_between_transports,
        cur_transits=cur_transits
    )

    __push_merge_event(
        _queue=_queue,
        cur_time=cur_time,
        speed=speed,
        photo_distance=photo_distance,
        rfid_distance=rfid_distance,
    )

    while _queue:
        __cur_time, __cur_event, __num_id = heappop(_queue)

        if __cur_event == _Event.PHOTO_TRANSIT:
            cur_time = __cur_time
            transit = generate_transit(
                cur_time=cur_time,
                sign_prob=sign_prob,
                num_prob=num_prob,
                speed=speed,
                distance=photo_distance,
                photo_error=photo_error,
                car_error=car_error
            )
            _Transits.append(transit)
        elif __cur_event == _Event.RFID_DETECTION:
            pass
        elif __cur_event == _Event.START_MERGE:
            # start merging and add
            pass
        else:
            raise Exception('Invalid event type')


def __get_photo_time(
    cur_time: float,
    speed: float,
    distance_between_transports: float
) -> float:
    return cur_time + distance_between_transports / speed


def __get_rfid_detection_time(
    cur_time: float,
    speed: float,
    photo_distance: float,
    rfid_distance: [float, float],
) -> float:
    return cur_time + photo_distance - (np.random.uniform(low=rfid_distance[0], high=rfid_distance[1])) / speed


def __push_rfid_detection_event(
    _queue: _EventQueue,
    cur_time: float,
    transit: Transit,
    rfid_distance: [float, float],
    cur_transits: int
):
    heappush(_queue, (
        __get_rfid_detection_time(
            cur_time=cur_time,
            speed=transit.speed,
            photo_distance=transit.photo_distance,
            rfid_distance=rfid_distance
        ),
        _Event.RFID_DETECTION,
        cur_transits
    ))


def __push_photo_event(
    _queue: _EventQueue,
    cur_time: float,
    speed: list[float, float],
    distance_between_transports: float,
    cur_transits: int
):
    heappush(_queue, (
        __get_photo_time(
            cur_time=cur_time,
            speed=np.random.uniform(low=speed[0], high=speed[1]),
            distance_between_transports=distance_between_transports
        ),
        _Event.PHOTO_TRANSIT,
        cur_transits
    ))


def __push_merge_event(
    _queue: _EventQueue,
    cur_time: float,
    speed: list[float, float],
    photo_distance: [float, float],
    rfid_distance: [float, float],
):
    heappush(_queue, (
        cur_time + (speed[0] + speed[1]) / (photo_distance[0] + photo_distance[1] - rfid_distance[1]),
        _Event.START_MERGE,
        None)
    )
