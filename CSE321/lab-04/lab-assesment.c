#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
    int status;
    pid_t my_pid, child_pid, grand_child_pid;
    my_pid = getpid();

    child_pid = fork();
    if (child_pid > 0)
    {
        wait(&status);
        printf("Parent running...\n");
    }
    else if (child_pid == 0)
    {
        grand_child_pid = fork();
        if (grand_child_pid > 0)
        {
            wait(&status);
            printf("Child running...\n");
        }
        else if (grand_child_pid == 0)
        {
            printf("Grand child running...\n");
        }
    }

    return 0;
}