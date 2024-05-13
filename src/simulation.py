from src.comparator import compare_transits_and_rfid_detections
from src.generator import generate_transit, generate_rfid_detection
from src.model import Transit, ModelResults, _EventQueue, _Transits, _RfidDetections, _Event
from heapq import heappush, heappop

import numpy as np

from src.utils import print_results


def simulate(
        sign_prob: dict[str, float],
        num_prob: dict[str, float],
        photo_distance: [float, float],
        rfid_distance: [float, float],
        speed: list[float, float],
        distance_between_transports: float,
        photo_error: float,
        rfid_error: float,
        car_error: float,
        num_transits=50_000
):
    assert 0 <= car_error <= 1
    assert 0 <= rfid_error <= 1
    assert 0 <= photo_error <= 1

    cur_time = 0
    cur_transits = 0

    _queue: _EventQueue = []  # use heappush and heappop
    transits: _Transits = [] # use transits
    rfid_detections: _RfidDetections = []

    results = ModelResults()

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

        # update internal time of the model
        cur_time = __cur_time

        # flag to stop simulation
        if cur_transits >= num_transits:
            break

        if __cur_event == _Event.PHOTO_TRANSIT:

            transit = generate_transit(
                cur_time=cur_time,
                sign_prob=sign_prob,
                num_prob=num_prob,
                speed=speed,
                distance=photo_distance,
                photo_error=photo_error,
                car_error=car_error
            )
            transits.append((transit, cur_transits))

            # event for rfid detection of this transit
            __push_rfid_detection_event(
                _queue=_queue,
                cur_time=cur_time,
                transit=transit,
                rfid_distance=rfid_distance,
                cur_transits=cur_transits
            )

            cur_transits = cur_transits + 1

            # event for next transit

            __push_photo_event(
                _queue=_queue,
                cur_time=cur_time,
                speed=speed,
                distance_between_transports=distance_between_transports,
                cur_transits=cur_transits
            )
        elif __cur_event == _Event.RFID_DETECTION:
            matches = [_transit for _transit in transits if _transit[1] == __num_id]

            if len(matches) == 0:
                raise Exception(f'Invalid num id: {__num_id}')

            cur_detection = generate_rfid_detection(
                time=cur_time,
                transit=matches[0][0],
                rfid_error=rfid_error,
            )

            rfid_detections.append((cur_detection, __num_id))
        elif __cur_event == _Event.START_MERGE:
            matched_transits, unmatched_transits = compare_transits_and_rfid_detections(
                transits=transits,
                detections=rfid_detections,
            )

            results.unmatched_transits = results.unmatched_transits
            results.matched_transits = results.matched_transits + matched_transits

            # update queues
            transits = unmatched_transits
            rfid_detections = []
            results.unmatched_transits = unmatched_transits

            # push next event to merge transits with rfid detections
            __push_merge_event(
                _queue=_queue,
                cur_time=cur_time,
                speed=speed,
                photo_distance=photo_distance,
                rfid_distance=rfid_distance,
            )
        else:
            raise Exception('Invalid event type')

    print_results(results)


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
    return cur_time + (photo_distance - (np.random.uniform(low=rfid_distance[0], high=rfid_distance[1]))) / speed


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
        cur_time + ((photo_distance[0] + photo_distance[1]) / 2 + rfid_distance[1]) / ((speed[0] + speed[1]) / 2),
        _Event.START_MERGE,
        None)
             )
