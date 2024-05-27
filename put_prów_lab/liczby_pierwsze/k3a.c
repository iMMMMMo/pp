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

    int blockSize = (int)(0.375 * 1024 * 1024);
    int numberOfBlocks = (n - m) / blockSize;
    if ((n - m) % blockSize != 0) { 
        numberOfBlocks++;
    }
    
    for (int i = 0; i < numberOfBlocks; i++) {
        int low = m + i * blockSize; 
        int high = m + i * blockSize + blockSize;
        if (high > n) {
            high = n;
        }
        for (int j = 2; j * j <= high; j++) {
            if (primeArray[j]) {
                int firstMultiple = (low / j);
                if (firstMultiple <= 1) {
                    firstMultiple = j + j;
                } else if (low % j) {
                    firstMultiple = (firstMultiple * j) + j;
                } else {
                    firstMultiple = (firstMultiple * j);
                }
                for (int k = firstMultiple; k <= high; k += j) {
                    result[k - m] = false;
                }
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
