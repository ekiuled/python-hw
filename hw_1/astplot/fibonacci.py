def fibonacci(n):
    result = [0, 1]
    for _ in range(2, n):
        result.append(result[-2] + result[-1])
    return result


if __name__ == '__main__':
    print(fibonacci(10))
