import dafsa


def build_dawg():
    with open('resources/twl06.txt', 'r') as file:
        words = [line.strip() for line in file if line.strip()]
    d=dafsa.DAFSA(words[:1000])
    return d