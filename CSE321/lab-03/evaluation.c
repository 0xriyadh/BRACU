#include <stdio.h>

int main()
{
    // taking two intergers as input
    int a, b;
    printf("Enter two integers: ");
    scanf("%d %d", &a, &b);

    // multiplying all the odd numbers between a and b
    int product = 1;
    for (int i = a + 1; i < b; i++)
    {
        if (i % 2 != 0)
        {
            product *= i;
        }
    }

    // printing the output in a new file
    FILE *output_file;
    output_file = fopen("output.txt", "w");
    fprintf(output_file, "The product of all odd numbers between %d and %d is %d", a, b, product);
    fclose(output_file);
}