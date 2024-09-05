#include <stdio.h>
#include <math.h>
// Function to check if a number is perfect

// without using math.h
// int isPerfect(int num) {
//     int sum = 0;
//     for (int i = 1; i <= num / 2; i++) {
//         if (num % i == 0) {
//             sum += i;
//         }
//     }
//     return sum == num;
// }

// using math.h
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

// Function to print perfect numbers in a given range
void printPerfectNumbers(int start, int end) {
    for (int i = start; i <= end; i++) {
        if (isPerfect(i)) {
            printf("%d\n", i);
        }
    }
}

int main() {
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