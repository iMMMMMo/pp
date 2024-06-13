#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <iostream>
#include <cmath>
#include <chrono>
#include <iomanip>

__global__ void computeOutput(float* input, float* output, int N, int R, int k) {
    int i = blockIdx.y * blockDim.y + threadIdx.y + R;
    int j = blockIdx.x * blockDim.x + threadIdx.x + R;

    if (i < N - R && j < N - R) {
        for (int idx = 0; idx < k; ++idx) {
            float sum = 0.0f;
            for (int di = -R; di <= R; ++di) {
                for (int dj = -R; dj <= R; ++dj) {
                    sum += input[(i + di) * N + (j + dj)];
                }
            }
            output[(i - R) * (N - 2 * R) + (j - R) + idx * (N - 2 * R) * (N - 2 * R)] = sum;
        }
    }
}

void computeSequential(float* input, float* output, int N, int R) {
    for (int i = R; i < N - R; ++i) {
        for (int j = R; j < N - R; ++j) {
            float sum = 0.0f;
            for (int di = -R; di <= R; ++di) {
                for (int dj = -R; dj <= R; ++dj) {
                    sum += input[(i + di) * N + (j + dj)];
                }
            }
            output[(i - R) * (N - 2 * R) + (j - R)] = sum;
        }
    }
}

int main() {
    // Parametry problemu
    int R = 1;    // Promień R
    int k = 1;    // Liczba wyników obliczanych przez jeden wątek

    for (int N = 640; N <= 1536; N += 128) {
        for (int multi = 2; multi <= 16; multi *= 2) {
            R = multi;
            k = multi;
            std::cout << "R=" << R << ", k=" << k << "\n";
            float* inputHost = new float[N * N];
            float* outputHostCPU = new float[(N - 2 * R) * (N - 2 * R)];
            float* outputHostGPU = new float[(N - 2 * R) * (N - 2 * R) * k];

            // Inicjalizacja danych wejściowych na CPU
            for (int i = 0; i < N * N; ++i) {
                inputHost[i] = static_cast<float>(rand()) / RAND_MAX;
            }

            // Obliczenia sekwencyjne dla porównania
            auto startCPU = std::chrono::high_resolution_clock::now();
            computeSequential(inputHost, outputHostCPU, N, R);
            auto endCPU = std::chrono::high_resolution_clock::now();
            std::chrono::duration<float> durationCPU = endCPU - startCPU;
            std::cout << "CPU Time for N=" << N << ": " << durationCPU.count() << "s\n";

            // Przygotowanie wskaźników na dane na GPU
            float* inputDevice, * outputDevice;
            cudaMalloc((void**)&inputDevice, N * N * sizeof(float));
            cudaMalloc((void**)&outputDevice, (N - 2 * R) * (N - 2 * R) * k * sizeof(float));

            // Kopiowanie danych z CPU do GPU
            cudaMemcpy(inputDevice, inputHost, N * N * sizeof(float), cudaMemcpyHostToDevice);

            // Określenie rozmiaru siatki wątków i bloków

            dim3 blockSize(32, 32);
            dim3 gridSize((N - 2 * R + blockSize.x - 1) / blockSize.x, (N - 2 * R + blockSize.y - 1) / blockSize.y);

            // Wywołanie kernela
            cudaEvent_t start, stop;
            cudaEventCreate(&start);
            cudaEventCreate(&stop);
            cudaEventRecord(start, 0);

            computeOutput << <gridSize, blockSize >> > (inputDevice, outputDevice, N, R, k);

            cudaEventRecord(stop, 0);
            cudaEventSynchronize(stop);

            float elapsedTime;
            cudaEventElapsedTime(&elapsedTime, start, stop);
            std::cout << "GPU Time for N=" << N << ": " << elapsedTime / 1000.0f << "s\n";

            // Kopiowanie wyników z GPU do CPU
            cudaMemcpy(outputHostGPU, outputDevice, (N - 2 * R) * (N - 2 * R) * k * sizeof(float), cudaMemcpyDeviceToHost);

            // Obliczanie FLOPS
            int numOps = (N - 2 * R) * (N - 2 * R) * (2 * R + 1) * (2 * R + 1);
            float flops = numOps / (elapsedTime / 1000.0f);
            printf("FLOP/s for N=%d: %.2e\n", N, flops);

            // Sprawdzenie poprawności obliczeń GPU poprzez porównanie z wynikami CPU
            float maxError = 0.0f;
            for (int i = 0; i < (N - 2 * R) * (N - 2 * R); ++i) {
                maxError = fmax(maxError, fabs(outputHostCPU[i] - outputHostGPU[i]));
            }

            if (maxError < 1e-5) {
                std::cout << "Poprawnosc obliczen GPU zostala zweryfikowana." << std::endl;
            }
            else {
                std::cout << "Blad obliczeń GPU! Maksymalny błąd: " << maxError << std::endl;
            }

            // Zwolnienie pamięci na GPU
            cudaFree(inputDevice);
            cudaFree(outputDevice);

            // Zwolnienie pamięci na CPU
            delete[] inputHost;
            delete[] outputHostCPU;
            delete[] outputHostGPU;

            std::cout << "--------------------------------------------" << std::endl;
        }
       
    }

    return 0;
}

