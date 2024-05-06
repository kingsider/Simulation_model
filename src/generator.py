import numpy as np

from src.model import Transit, RfidDetection
from src.utils import check_probs


def generate_plate(sign_prob: dict[str, float], num_prob: dict[str, float]) -> str:

    assert abs(sum(sign_prob.values()) - 1) < 1e-6
    assert abs(sum(num_prob.values()) - 1) < 1e-6

    check_probs(sign_prob)
    check_probs(num_prob)

    plate_sign = ''
    for _ in range(2):
        plate_sign += generate_sign(sign_prob)

    plate_num = ''
    for _ in range(3):
        plate_num += generate_sign(num_prob)

    return plate_sign + plate_num + generate_sign(sign_prob)


def generate_sign(probs: dict[str, float]) -> str:
    generation = np.random.uniform()

    cur = 0
    for key in probs:
        cur += probs[key]

        if generation <= cur:
            return key


def generate_transit(
        cur_time: float,
        sign_prob: dict[str, float],
        num_prob: dict[str, float],
        speed: list[float, float],
        distance: list[float, float],
        photo_error: float,
        car_error: float,
) -> Transit:
    num = generate_plate(sign_prob=sign_prob, num_prob=num_prob)
    photo_num = num

    _speed = np.random.uniform(low=speed[0], high=speed[1])

    num_val = []
    for i, value in enumerate(list(photo_num)):
        if np.random.uniform(low=0, high=1) <= photo_error:
            num_val.append('*')
        else:
            num_val.append(value)

    photo_num = ''.join(num_val)

    _photo_distance = np.random.uniform(low=distance[0], high=distance[1])

    car_model_detected = np.random.uniform(low=0, high=1) > car_error

    return Transit(
        num=num,
        photo_num=photo_num,
        photo_detection_time=cur_time,
        photo_distance=_photo_distance,
        speed=_speed,
        car_model_detected=car_model_detected
    )


def generate_rfid_detection(
        time: float,
        transit: Transit,
        rfid_error: float,
) -> RfidDetection:
    if np.random.uniform(low=0, high=1) <= rfid_error:
        return RfidDetection(rfid_detection_time=time, rfid_num=None)
    return RfidDetection(rfid_detection_time=time, rfid_num=transit.num)
