#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "a");
    if (file == NULL)
    {
        perror("Error opening file");
        return 1;
    }

    char input[256];
    while (1)
    {
        printf("Enter a string (or -1 to exit): ");
        fgets(input, sizeof(input), stdin);

        if (input[0] == '-' && input[1] == '1' && (input[2] == '\n' || input[2] == '\0'))
        {
            break;
        }

        fprintf(file, "%s", input);
    }

    fclose(file);
    return 0;
}