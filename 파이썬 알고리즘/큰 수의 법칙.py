def solution():
    print("배열의 크기, 덧셈 횟수, 큰수 연속 덧셈 횟수")
    n, m, k = map(int, input().split())
    while 1:
        print("데이터 입력:")
        data = list(map(int, input().split()))
        if len(data) != n:
            print('잘못 입력하였습니다. 배열의 크기에 맞게 입력해주세요')
            continue
        else: break

    data.sort()
    first = data[n-1] # 가장 큰수
    second = data[n-2]

    result = 0
    while 1:
        for i in range(k):
            if m == 0:
                break
            result += first
            m -= 1
        if m == 0:
            break
        result += second
        m -= 1
    return result

print(solution())