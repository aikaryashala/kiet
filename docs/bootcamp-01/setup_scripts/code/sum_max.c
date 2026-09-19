#include <stdio.h>

int max_of_two(int num1, int num2);
int sum_of_two(int num1, int num2);

int main()
{
    int num1, num2;
    int max, sum;
    num1 = 2;
    num2 = 3;

    max_of_two(num1, num2);
    sum_of_two(num1, num2);
    return 0;
}

int max_of_two(int num1, int num2)
{
    int max;

    if (num2 > num1)
    {
    	max = num2;
    }
    else
    {
    	max = num1;
    }
    printf("%d is greater.\n", max);
    return 0;
}

int sum_of_two(int num1, int num2)
{
    int sum;
    sum = num1 + num2;
    printf("Sum of numbers is %d.\n", sum);
    return 0;
}
