# Дополнительное задание: перевод числа из десятичной системы счисления в фибоначчиеву
def dec_to_fib(n: int) -> int:
    fib = [1, 2]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    if fib[-1] > n:
        fib.pop()
    result = []
    skip_next = False
    for f in reversed(fib):
        if skip_next:
            result.append(0)
            skip_next = False
            continue
        if f <= n:
            result.append(1)
            n -= f
            skip_next = True
        else:
            result.append(0)
    return int(''.join(map(str, result)))


print(dec_to_fib(int(input())))
