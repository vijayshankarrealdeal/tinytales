import random

def generate_random_ids(min_id, max_id, limit):
    return random.sample(range(min_id, max_id + 1), k=limit)
