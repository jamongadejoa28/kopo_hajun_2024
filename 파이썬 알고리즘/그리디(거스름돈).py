def solution(n):
    coin_types = [500,100,50,10]
    count = 0
    for coin in coin_types:
        count += n // coin
        n %= coin
    return count
print(solution(1260))