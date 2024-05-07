from src.model import Transit, RfidDetection

def compare_transits_and_rfid_detections(
    transits: list[Transit],
    detections: list[RfidDetection]
) -> int:
    matched_numbers = set()

    for detection in detections:
        if detection.rfid_num is not None:

            for transit in transits:
                if transit.num == detection.rfid_num:
                    matched_numbers.add(transit.num)
                    break

    unmatched_count = len(detections) - len(matched_numbers)
    return unmatched_count
pass