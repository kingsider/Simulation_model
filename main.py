from src.simulation import simulate

sign_prob = {
    'A': 0.1,
    'B': 0.1,
    'C': 0.1,
    'D': 0.1,
    'E': 0.1,
    'T': 0.1,
    'P': 0.1,
    'M': 0.1,
    'K': 0.1,
    'O': 0.1
}

num_prob = {
    '0': 0.1,
    '1': 0.1,
    '2': 0.1,
    '3': 0.1,
    '4': 0.1,
    '5': 0.1,
    '6': 0.1,
    '7': 0.1,
    '8': 0.1,
    '9': 0.1
}

photo_distance = [30, 50] # meters
rfid_distance = [-5, 5] # meters
speed = [60 / 3.6, 100 / 3.6] # meters per hour

distance_between_transports = 10 # meters

photo_error = 0.1
rfid_error = 0.05
car_error = 0.1

simulate(
    sign_prob=sign_prob,
    num_prob=num_prob,
    photo_distance=photo_distance,
    rfid_distance=rfid_distance,
    speed=speed,
    distance_between_transports=distance_between_transports,
    photo_error=photo_error,
    rfid_error=rfid_error,
    car_error=car_error
)