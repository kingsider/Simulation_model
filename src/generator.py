import numpy as np

def check_probs(probs: dict[str, float]):
    for value in probs.values():
        assert 0 <= value <= 1

def generate_plate(sign_prob: dict[str, float], num_prob: dict[str, float]) -> str:

    assert abs(sum(sign_prob.values()) - 1) < 1e-6
    assert abs(sum(num_prob.values()) - 1) < 1e-6

    check_probs(sign_prob)
    check_probs(num_prob)

    plate_sign = ''
    for _ in range(3):
        plate_sign += generate_sign(sign_prob)

    plate_num = ''
    for _ in range(3):
        plate_num += generate_sign(num_prob)

def generate_sign(probs: dict[str, float]) -> str:
    generation = np.random.uniform()

    cur = 0
    for key in probs:
        cur += probs[key]

        if generation <= cur:
            return key

    return None

