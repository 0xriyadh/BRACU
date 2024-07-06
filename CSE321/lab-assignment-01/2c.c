#include <stdio.h>

int main()
{
    char password[100];
    printf("Enter the password: ");
    fgets(password, sizeof(password), stdin);

    // check if the password has:
    // - At least one lowercase letter
    // - At least one uppercase letter
    // - At least one digit (0-9)
    // - At least one special character (_ , $, #, @)
    int has_lowercase = 0, has_uppercase = 0, has_digit = 0, has_special = 0;
    for (int i = 0; password[i] != '\0'; i++)
    {
        if (password[i] >= 'a' && password[i] <= 'z')
        {
            has_lowercase = 1;
        }
        if (password[i] >= 'A' && password[i] <= 'Z')
        {
            has_uppercase = 1;
        }
        if (password[i] >= '0' && password[i] <= '9')
        {
            has_digit = 1;
        }
        if (password[i] == '_' || password[i] == ',' || password[i] == '$' || password[i] == '#' || password[i] == '@')
        {
            has_special = 1;
        }
    }
    if (has_lowercase && has_uppercase && has_digit && has_special)
    {
        printf("OK\n");
    }
    else
    {
        if (!has_lowercase)
        {
            printf("Lowercase character missing\n");
        }
        if (!has_uppercase)
        {
            printf("Uppercase character missing\n");
        }
        if (!has_digit)
        {
            printf("Digit missing\n");
        }
        if (!has_special)
        {
            printf("Special character missing\n");
        }
    }
    return 0;
}