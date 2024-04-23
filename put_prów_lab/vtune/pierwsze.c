#include <stdio.h>
#include <omp.h>

#define NUM 100000000

int isprime( int x )
{
    for( int y = 3; y * y <= x; y+=2 )
    {
        if( x % y == 0 )
            return 0;
    }

    return 1;
}

int main( )
{
    int sum = 0;

#pragma omp parallel for schedule(static, 100) reduction (+:sum)
    for( int i = 3; i <= NUM ; i+=2 )
    {
        sum += isprime ( i );
    }

    printf( "Number of primes numbers: %d", sum+1 );

    return 0;
}

