#include <stdio.h>
#include <string.h>

int main() 
{
    char str[100];
    char *start, *end;
    int isPalindrome = 1; // assuming the input string is a palindrome

    printf("Enter a string: ");
    fgets(str, sizeof(str), stdin);
    str[strcspn(str, "\n")] = 0;

    start = str;
    end = str + strlen(str) - 1;

    while (start < end) {
        if (*start != *end) {
            isPalindrome = 0;
            break;
        }
        start++;
        end--;
    }

    if (isPalindrome) {
        printf("Palindrome\n");
    } else {
        printf("Not Palindrome\n");
    }
}