import numpy as np

def generate_plate(sign_prob: dict[str, float], num_prob: dict[str, float]) -> str:
    assert abs(sum(sign_prob.values()) - 1) < 1e-6
    assert abs(sum(num_prob.values()) - 1) < 1e-6

    plate_sign = ''
    for _ in range(3):
        plate_sign += generate_sign(sign_prob)

    plate_num = ''
    for _ in range(3):
        plate_num += generate_sign(num_prob)

    return plate_sign[0] + plate_num[:3] + plate_sign[1:] + plate_num[3:]

    pass
def generate_sign(probs: dict[str, float]) -> str:
    generation = np.random.uniform()

    cur = 0
    for key in probs:
        cur += probs[key]

        if generation <= cur:
            return key

    return None

sign_prob = {'A': 0.085,
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
             'У': 0.083}

num_prob = {'0': 0.1,
            '1': 0.1,
            '2': 0.1,
            '3': 0.1,
            '4': 0.1,
            '5': 0.1,
            '6': 0.1,
            '7': 0.1,
            '8': 0.1,
            '9': 0.1}

plate_number = generate_plate(sign_prob, num_prob)
print(plate_number)
