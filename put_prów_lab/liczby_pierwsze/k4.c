#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <omp.h>
#include <string.h>

void findPrimesInRange(int m, int n, int printPrimes) {
    bool* result = (bool*)malloc((n - m + 1) * sizeof(bool));
    memset(result, true, (n - m + 1) * sizeof(bool));
    bool* primeArray = (bool*)malloc((n + 1) * sizeof(bool));
    memset(primeArray, true, (n + 1) * sizeof(bool));

    for (int i = 2; i * i * i * i <= n; i++) {
        if (primeArray[i] == true) {
            for (int j = i * i; j * j <= n; j += i) {
                primeArray[j] = false;
            }
        }
    }

    int sqrt_n = (int)sqrt(n);

    omp_set_num_threads(8);
    #pragma omp parallel for schedule(dynamic)
    for (int i = 2; i <= sqrt_n; i++) {
        if (primeArray[i]) {
            int firstMultiple = (m / i);
            if (firstMultiple <= 1) {
                firstMultiple = i + i;
            } else if (m % i) {
                firstMultiple = (firstMultiple * i) + i;
            } else {
                firstMultiple = (firstMultiple * i);
            }
            for (int j = firstMultiple; j <= n; j += i) {
                result[j - m] = false;
            }
        }
    }

    int numOfPrimesInBetween = 0;
    int lineCounter = 0;

    if (printPrimes) {
        printf("Prime numbers between %d and %d:\n", m, n);
        for (int i = m; i <= n; i++) {
            if (result[i - m] == true) {
                printf("%d ", i);
                numOfPrimesInBetween++;
                lineCounter++;
            }

            if (lineCounter == 10) {
                printf("\n");
                lineCounter = 0;
            }
        }
        printf("\n");
    } else {
        for (int i = m; i <= n; i++) {
            if (result[i - m] == true) {
                numOfPrimesInBetween++;
            }
        }
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
