def check_probs(probs: dict[str, float]):
    for value in probs.values():
        assert 0 <= value <= 1