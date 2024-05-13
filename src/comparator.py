from src.model import Transit, RfidDetection

def compare_transits_and_rfid_detections(
    transits: list[Transit],
    detections: list[RfidDetection]
) -> (int, int):
    matched_numbers = set()
    successful_merges = 0

    for detection in detections:
        if detection.rfid_num is not None:

            matching_transits = [transit for transit in transits if transit.num == detection.rfid_num]

            if len(matching_transits) == 1:
                matched_numbers.add(detection.rfid_num)

                if matching_transits[0].car_model_detected:
                    successful_merges += 1
            elif len(matching_transits) > 1:

                # если несколько совпадений
                for transit in matching_transits:
                    if transit.car_model_detected:
                        matched_numbers.add(detection.rfid_num)
                        successful_merges += 1
                        break

    unmatched_count = len(detections) - len(matched_numbers)
    return unmatched_count, successful_merges
