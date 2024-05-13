from src.model import Transit, RfidDetection, _Transits, _RfidDetections
from src.utils import find_match_num_id


def compare_transits_and_rfid_detections(
    transits: _Transits,
    detections: _RfidDetections
) -> (list[Transit], list[Transit]):
    matched_transits: list[_Transits] = list()
    unmatched_transits: list[_Transits] = list()

    for (detection, num_id) in detections:
        if detection.rfid_num is not None:

            _matched_transits = [_transit for _transit in transits if _transit[0].num == detection.rfid_num]

            # if len(_matched_transits) == 0:
            #     match = find_match_num_id(num_id=num_id, transits=transits)
            #     unmatched_transits.append(match)

            if len(_matched_transits) == 1:
                matched_transits.append(_matched_transits[0])

            elif len(_matched_transits) > 1:
                for transit in _matched_transits:
                    if transit[0].car_model_detected:
                        _match = find_match_num_id(num_id=num_id, transits=_matched_transits)
        # else:
        #     match = find_match_num_id(num_id=num_id, transits=transits)
        #     unmatched_transits.append(match)

    for transit in transits:
        if find_match_num_id(num_id=transit[1], transits=matched_transits) is None:
            unmatched_transits.append(transit)

    return matched_transits, unmatched_transits
