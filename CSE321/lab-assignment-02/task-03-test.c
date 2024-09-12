#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

int main()
{
    // the main PID
    printf("Main PID: %d\n", getpid());
    pid_t child_pid, grandchild_pid;

    // Create one child process
    child_pid = fork();

    if (child_pid < 0)
    {
        perror("fork");
        return 1;
    }
    else if (child_pid == 0)
    {
        // Child process
        printf("Child process ID: %d, Parent process ID: %d\n", getpid(), getppid());

        // Create three grandchild processes
        for (int i = 0; i < 3; i++)
        {
            grandchild_pid = fork();

            if (grandchild_pid < 0)
            {
                perror("fork");
                return 1;
            }
            else if (grandchild_pid == 0)
            {
                // Grandchild process
                printf("Grandchild process ID: %d, Parent process ID: %d\n", getpid(), getppid());
                exit(0); // Grandchild process exits
            }
            else
            {
                // Child process waits for each grandchild to finish
                waitpid(grandchild_pid, NULL, 0);
            }
        }
        exit(0); // Child process exits after creating grandchildren
    }
    else
    {
        // Parent process waits for the child to finish
        waitpid(child_pid, NULL, 0);
    }

    return 0;
}