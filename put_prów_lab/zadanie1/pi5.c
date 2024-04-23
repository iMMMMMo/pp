#include <stdio.h>
#include <time.h>
#include <omp.h>

long long num_steps = 100000000;
double step;

int main(int argc, char* argv[])
{
	clock_t spstart, spstop,ppstart,ppstop;
	double sswtime, sewtime, pswtime, pewtime;

	//volatile
	double x, pi, sum=0.0;
	int i;

	//SEKWENCYJNIE
	sswtime = omp_get_wtime();
	spstart = clock();

	step = 1.0 / (double)num_steps;

	for (i = 0; i < num_steps; i++)
	{
		x = (i + 0.5) * step;
		sum = sum + 4.0 / (1.0 + x*x);
	}
	
	pi = sum*step;

	spstop = clock();
    sewtime = omp_get_wtime();
    printf("--> %15.12f Wartosc liczby PI sekwencyjnie \n", pi);
  
	//liczba wątków
	omp_set_num_threads(8);

	//RÓWNOLEGLE 
	pswtime = omp_get_wtime();
	ppstart = clock();
	sum = 0.0;
	step = 1.0 / (double)num_steps;

	#pragma omp parallel reduction(+:sum)
	{
		#pragma omp for
		for (i = 0; i < num_steps; i++)
		{
            double x = (i + 0.5) * step;
			sum += + 4.0 / (1.0 + x*x);
		}
	}
	pi = sum * step;

	ppstop = clock();
	pewtime = omp_get_wtime();

	printf("--> %15.12f Wartosc liczby PI rownolegle \n",pi);
	printf("Czas procesorow przetwarzania sekwencyjnego - %f sekund \n", ((double)(spstop - spstart)/CLOCKS_PER_SEC));
	printf("Czas procesorow przetwarzania rownoleglego - %f sekund \n", ((double)(ppstop - ppstart)/CLOCKS_PER_SEC));
	printf("Czas trwania obliczen sekwencyjnych - wallclock %f sekund \n",  sewtime-sswtime);
	printf("Czas trwania obliczen rownoleglych - wallclock %f sekund \n", pewtime-pswtime);
	printf("Przyspieszenie %5.3f \n", (sewtime - sswtime) / (pewtime - pswtime));
	return 0;
}