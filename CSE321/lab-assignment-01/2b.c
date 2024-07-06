#include <stdio.h>
#include <string.h>

int main()
{
    FILE *input_file, *output_file;
    char input[100];
    char divider[] = " ";
    char *token;
    int lines = 0;

    input_file = fopen("2b-input.txt", "r");
    output_file = fopen("2b-output.txt", "w");

    while (fgets(input, sizeof(input), input_file) != NULL)
    {
        lines++;
        char newline[100] = "";

        // getting the first token
        token = strtok(input, divider);
        strcat(newline, token);

        // getting the rest of the tokens
        while (token != NULL)
        {
            token = strtok(NULL, divider);
            if (token != NULL)
            {
                strcat(newline, " ");
                strcat(newline, token);
            }
        }
        fprintf(output_file, "line %d: %s", lines, newline);
    }

    fclose(input_file);
    return 0;
}