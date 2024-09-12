#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

int main()
{
    // the main PID
    // printf("Main PID: %d\n", getpid());

    pid_t a, b, c;
    int pipe_msg = 0;
    int fd[2];
    pipe(fd); // defining pipe for interprocess communication

    a = fork();
    // printf("a is %d and forked by %d\n", a, getpid());
    b = fork();
    // printf("b is %d and forked by %d\n", b, getpid());
    c = fork();
    // printf("c is %d and forked by %d\n", c, getpid());

    if (a == 0 && (b > 0 && c > 0))
    {
        waitpid(b, NULL, 0);
        waitpid(c, NULL, 0);
    }
    else if (b == 0 && c > 0)
    {
        waitpid(c, NULL, 0);
    }

    // printing all the PIDs
    // printf("a: %d, b: %d, c: %d, from parent: %d\n", a, b, c, getpid());

    if (a > 0 && b > 0 && c > 0)
    {

        // waiting for all the child process to finish their execution
        while (wait(NULL) != -1 || errno != ECHILD)
            ;

        close(fd[1]);

        int total_processes = 1;

        while (read(fd[0], &pipe_msg, sizeof(int)) != 0)
        {
            total_processes++;
        }
        printf("Total processes: %d\n", total_processes);
        close(fd[0]);
    }
    else
    {

        printf("I am child %d my parent is %d\n", getpid(), getppid());
        write(fd[1], &pipe_msg, sizeof(int));
        pid_t grand_child = -1;

        if (getpid() % 2)
        {
            grand_child = fork();
            if (grand_child == 0)
            {
                write(fd[1], &pipe_msg, sizeof(int));
                printf("Inside fork %d my parent %d\n", getpid(), getppid());
                return 0;
            }
        }

        // waiting for grand child process to finish its execution
        if (grand_child != -1)
        {
            waitpid(grand_child, NULL, 0);
        }

        return 0;
    }

    return 0;
}