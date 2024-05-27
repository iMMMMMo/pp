#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <omp.h>
#include <string.h>

void findPrimesInRange(int m, int n, int printPrimes) {
    bool* result = (bool*)malloc((n - m + 1) * sizeof(bool));
    memset(result, true, (n - m + 1) * sizeof(bool));
    bool* primeArray = (bool*)malloc((sqrt(n) + 1) * sizeof(bool));
    memset(primeArray, true, (sqrt(n) + 1) * sizeof(bool));

    for (int i = 2; i * i <= n; i++) {
        for (int j = 2; j * j <= i; j++) {
            if (primeArray[j] == true && i % j == 0) {
                primeArray[i] = false;
                break;
            }
        }
    }

    int numOfPrimesInBetween = 0;

    for (int i = m; i <= n; i++) {
        bool isPrime = true;
        for (int j = 2; j * j <= i; j++) {
            if (primeArray[j] == true && i % j == 0) {
                result[i - m] = false;
                isPrime = false;
                break;
            }
        }
        if (isPrime && i >= 2) {
            numOfPrimesInBetween++;
        }
    }

    if (printPrimes) {
        printf("Prime numbers between %d and %d:\n", m, n);
        for (int i = 0; i <= n - m; i++) {
            if (result[i] == true) {
                printf("%d ", m + i);
            }
        }
        printf("\n");
    }

    printf("%d\n", numOfPrimesInBetween);
    // printf("Primes found between %d-%d: %d\n", m, n, numOfPrimesInBetween);

    free(result);
    free(primeArray);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Usage: %s <m> <n> <printPrimes>\n", argv[0]);
        return 1;
    }

    int m = atoi(argv[1]);
    int n = atoi(argv[2]);
    int printPrimes = atoi(argv[3]);
    double startTime;
    double stopTime;

    if (m < 2 || n < 2 || m > n) {
        printf("Invalid range. Both m and n should be integers greater than 1, and m should be less than or equal to n.\n");
        return 1;
    }

    startTime = omp_get_wtime();
    findPrimesInRange(m, n, printPrimes);
    stopTime = omp_get_wtime();

    printf("%g\n", stopTime-startTime);
    // printf("Time: %g\n", stopTime-startTime);

    return 0;
}
