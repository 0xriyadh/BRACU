#include <stdio.h>

int main()
{   
    FILE *input_file, *output_file;
    int lines = 0;
    
    input_file = fopen("2b-input.txt", "r");
    
    while (!feof(input_file)) {
        char input[100];
        fgets(input, sizeof(input), input_file);
        lines++;
        printf("line %d: %s", lines, input);
    }
    
    fclose(input_file);
    return 0;
}