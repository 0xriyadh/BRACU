#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    pid_t pid1, pid2;

    pid1 = fork(); // child process

    if (pid1 == 0)
    {
        // Child process
        pid2 = fork(); // grandchild process

        if (pid2 == 0)
        {
            // Grandchild process
            printf("I am grandchild\n");
        }
        else
        {
            // waiting for grandchild to finish
            wait(NULL);
            printf("I am child\n");
        }
    }
    else
    {
        // waiting for child to finish
        wait(NULL);
        printf("I am parent\n");
    }

    return 0;
}