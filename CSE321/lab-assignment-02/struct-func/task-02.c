#include <stdio.h>
#include <math.h>

// this function checks if a number is perfect or not
int isPerfect(int num)
{
    if (num < 2)
        return 0; // No perfect numbers less than 2

    int sum = 1; // 1 is a divisor of every number
    int sqrt_num = (int)sqrt(num);

    for (int i = 2; i <= sqrt_num; i++)
    {
        if (num % i == 0)
        {
            sum += i;
            if (i != num / i)
            {
                sum += num / i;
            }
        }
    }

    return sum == num;
}

// this function prints perfect numbers in the given range
void printPerfectNumbers(int start, int end)
{
    for (int i = start; i <= end; i++)
    {
        if (isPerfect(i))
        {
            printf("%d\n", i);
        }
    }
}

int main()
{
    int start, end;

    // Input for the range
    printf("Enter the start of the range: ");
    scanf("%d", &start);
    printf("Enter the end of the range: ");
    scanf("%d", &end);

    // Print perfect numbers in the given range
    printPerfectNumbers(start, end);

    return 0;
}