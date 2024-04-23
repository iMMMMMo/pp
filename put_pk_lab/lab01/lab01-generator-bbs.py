import math
import random

def main():
    while True:
        p = int(input("Podaj wartość p: "))
        q = int(input("Podaj wartość q: "))
        if check_params(p, q):
            break
    # p = 10007
    # q = 10039
    print(f"P wynosi {p}")
    print(f"Q wynosi {q}")
    N = p * q
    print(f"N wynosi {N}")

    while True:
        x = random.randint(1000, 9999)
        if math.gcd(x, N) == 1:
            break
    print(f"X wynosi {x}")

    x0 = pow(x, 2, N)

    lsb_list = bbs_generator(20000, x0, N)

    print("\n-- Test pojedynczych bitów (wynik testu, ilosc) --")
    print("Ilosc jedynek w kodzie: ", single_bit_test(lsb_list, 1))

    print("\n-- Test serii i długiej serii (wynik testu serii, liczba podciagow, wynik testu dlugiej serii) --")
    print("Podciagi zer: ", series_test(lsb_list, 0))
    print("Podciagi jedynek: ", series_test(lsb_list, 1))

    print("\n-- Test pokerowy (wynik testu, ilosc wystapien, wartosc x) --")
    print(poker_test(lsb_list))
    
def is_prime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
        return True
    else:
        return False
    
def check_params(p, q):
    if p < 1000 or q < 1000 or not is_prime(p) or not is_prime(q):
        return False
    return p % 4  == 3 and q % 4 == 3

def bbs_generator(size, x, N):
    bits = []
    bits.append(x % 2)
    for i in range(1, size):
        x = pow(x, 2, N)
        bits.append(x % 2)
    
    return bits

def single_bit_test(bits, n):
    return (9725 < bits.count(n) < 10275, bits.count(n))

def series_test(bits, n):
    series = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    current_series = 0
    long_series = False
    for bit in bits:
        if bit == n:
            current_series += 1
        else:
            if current_series >= 26:
                long_series = True
            if current_series > 6:
                series[6] += 1
            elif current_series > 0:
                series[current_series] += 1
            current_series = 0

    if (2315 < series[1] < 2685 and 
        1114 < series[2] < 1386 and 
        527 < series[3] < 723 and 
        240 < series[4] < 384 and 
        103 < series[5] < 209 and 
        103 < series[6] < 209):
        return (True, series, long_series)
    return (False, series, long_series)

def poker_test(bits):
    segmented_bits = [bits[i:i+4] for i in range(0, len(bits), 4)]

    counts = {i: 0 for i in range(16)}

    for segment in segmented_bits:
        val = int(''.join(map(str, segment)), 2) 
        counts[val] += 1

    x = (16/5000) * sum([pow(val, 2) for val in counts.values()]) - 5000

    return (2.16 < x < 46.17, counts, round(x, 2))

if __name__ == "__main__":
    main()