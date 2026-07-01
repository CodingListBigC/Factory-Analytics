import math


itemWidth = 50


def title(title: str):
    title_lenght = len(title)
    amount = math.floor((itemWidth - title_lenght - 2) / 2)
    print(f"{'-' * amount} {title} {'-' * amount}")
