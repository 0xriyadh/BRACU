#include <stdio.h>
#include <string.h>

int main() {
    char email[100];
    char divider[] = "@";
    char *email_first_portion, *email_second_portion;

    printf("Enter your email: ");
    fgets(email, sizeof(email), stdin);

    email_first_portion = strtok(email, divider);
    email_second_portion = strtok(NULL, divider);
    
    if (strcmp(email_second_portion, "sheba.xyz\n") == 0)
    {
        printf("Email address is okay\n");
    }
    else
    {
        printf("Email address is outdated\n");
    }

    return 0;
}