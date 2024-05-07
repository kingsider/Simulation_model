from src.model import ModelParams, Transit, RfidDetection
from src.generator import generate_transit, generate_rfid_detection

model_params = ModelParams(
    sign_prob={'A': 0.085,
               'B': 0.084,
               'C': 0.084,
               'E': 0.083,
               'H': 0.083,
               'K': 0.083,
               'M': 0.083,
               'O': 0.083,
               'P': 0.083,
               'T': 0.083,
               'X': 0.083,
               'У': 0.083},

    num_prob={'0': 0.1,
              '1': 0.1,
              '2': 0.1,
              '3': 0.1,
              '4': 0.1,
              '5': 0.1,
              '6': 0.1,
              '7': 0.1,
              '8': 0.1,
              '9': 0.1},

    average_speed=60 / 3.6,
    transport_distance=100,
    photo_distance=100,
    rfid_distance=10,
    photo_error=0.05,
    rfid_error=0.01
)

transits = [generate_transit(
    cur_time=i,
    sign_prob=model_params.sign_prob,
    num_prob=model_params.num_prob,
    speed=[model_params.average_speed - 5, model_params.average_speed + 5],
    distance=[model_params.transport_distance - 10, model_params.transport_distance + 10],
    photo_error=model_params.photo_error,
    car_error=0.1
) for i in range(10)]

detections = [generate_rfid_detection(
    transit=transits[i],
    time=i,
    rfid_error=model_params.rfid_error
) for i in range(10)]


def compare_transits_and_rfid_detections(transits: list[Transit], detections: list[RfidDetection]):
    unmatched_count = 0
    matched_transits = set()

    transits.sort(key=lambda x: x.photo_detection_time)
    detections.sort(key=lambda x: x.rfid_detection_time)

    for detection in detections:
        match_found = False
        if detection.rfid_num is not None:
            for transit in transits:

                expected_rfid_time = transit.photo_detection_time + (
                            model_params.photo_distance + model_params.rfid_distance) / model_params.average_speed

                if (transit.num == detection.rfid_num and
                        abs(expected_rfid_time - detection.rfid_detection_time) <= (
                                transit.photo_distance / transit.speed)):
                    match_found = True
                    matched_transits.add(transit)
                    break
        if not match_found:
            unmatched_count += 1

    return unmatched_count, matched_transits
    pass
