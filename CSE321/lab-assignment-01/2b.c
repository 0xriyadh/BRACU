#include <stdio.h>

int main()
{   
    FILE *input_file, *output_file;
    char input[100];
    
    input_file = fopen("2b-input.txt", "w+");
    fscanf(input_file, "%s", input);
    fclose(input_file);

    printf("input: %s\n", input);

    // output_file = fopen("2b-output.txt", "w+");
    // fprintf(output_file, "%s", input);
    // fclose(output_file);

    return 0;
}