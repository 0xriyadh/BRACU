#include <stdio.h>

int main()
{
    int a, b;
    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);
    
    if (a > b) {
        int sub = a - b;
        printf("Subtraction of %d and %d is %d\n", a, b, sub);
    } else if (a < b) {
        int sum = a + b;
        printf("Sum of %d and %d is %d\n", a, b, sum);
    } else {
        int mul = a * b;
        printf("Multiplication of %d and %d is %d\n", a, b, mul);
    }

    return 0; 
}