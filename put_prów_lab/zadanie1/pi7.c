#include <stdio.h>
#include <time.h>
#include <omp.h>

long long num_steps = 10000000;
double step;

int main(int argc, char* argv[])
{
	clock_t spstart, spstop,ppstart,ppstop;
	double sswtime, sewtime, pswtime, pewtime;

	//volatile
	double x, pi, sum=0.0;
	int i;
  
	//liczba wątków
    const int num_threads = 2;
	omp_set_num_threads(num_threads);

	//RÓWNOLEGLE 
    const int tab_size = 50;
    double tab[tab_size];

    for (int j = 0; j < tab_size; j++)
    {
        pswtime = omp_get_wtime();
        ppstart = clock();
        sum = 0.0;
        step = 1.0 / (double)num_steps;
        #pragma omp parallel
        {
            int thread_id = omp_get_thread_num();
            tab[thread_id + j] = 0; 
            #pragma omp for
            for (i = 0; i < num_steps; i++)
            {
                double x = (i + 0.5) * step;
                #pragma omp flush
                tab[thread_id + j] += 4.0 / (1.0 + x*x);
            }

            #pragma omp atomic
            sum += tab[thread_id + j];
            pi = sum * step;
	    }

        ppstop = clock();
	    pewtime = omp_get_wtime();

        printf("%d.  %f sekund\n", j, ((double)(ppstop - ppstart)/CLOCKS_PER_SEC));
    }
	return 0;
}