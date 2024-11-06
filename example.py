from rfbp import rfbp


def loader():
    for x in range(4):
        yield x


def transformer(x):
    import random

    if random.random() < 0.5:
        raise ValueError("mock exception")
    return x * 2


if __name__ == "__main__":
    result = rfbp(loader(), transformer, failfast=False)
    print(result)
