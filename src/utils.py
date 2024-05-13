from src.model import Transit, ModelResults, _Transits


def check_probs(probs: dict[str, float]):
    for value in probs.values():
        assert 0 <= value <= 1


def find_match_num_id(num_id: int, transits: _Transits) -> (int, Transit):
    matches = [_transit for _transit in transits if _transit[1] == num_id]

    if len(matches) == 0:
        return None

    if len(matches) > 1:
        raise Exception(f'Invalid num_id: {num_id}, find a few matches')

    return matches[0]


def print_results(result: ModelResults):
    print(f"""
        matched_transits={len(result.matched_transits)}
        unmatched_transits={len(result.unmatched_transits)}
        detection_probability={len(result.matched_transits) / (len(result.matched_transits) + len(result.unmatched_transits))}
    """)
