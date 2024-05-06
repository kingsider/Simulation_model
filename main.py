from src.generator import generate_sign, generate_transit

print(generate_sign({'A': 0.1, 'B': 0.9}))

print(generate_transit(
    0,
{'A': 0.1, 'B': 0.9},
    {'1': 0.1, '2': 0.9},
    [70, 90],
    [20, 30],
    [-5, 5],
    0.1,
    0.05,
    0.05
))