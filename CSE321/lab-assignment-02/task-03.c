#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

#define SHM_NAME "/process_count_shm"

void create_child_if_odd(pid_t pid, int *count)
{
    // checking if the PID is odd
    // printf("Checking if PID is odd: %d\n", pid);
    if (pid % 2 != 0)
    {
        // if PID is odd, create a new child process
        // printf("PID is odd, creating a new child process\n");
        pid_t new_child = fork();
        if (new_child == 0)
        {
            // child process
            (*count)++;
            printf("New child process created with PID: %d\n", getpid());
            exit(0);
        }
        else if (new_child > 0)
        {
            // parent process
            waitpid(new_child, NULL, 0); // waiting for the new child to finish
        }
        else
        {
            perror("Fork failed");
            exit(1);
        }
    }
}

int main()
{
    pid_t a, b, c;

    // creating shared memory
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1)
    {
        perror("shm_open");
        exit(1);
    }

    // configuring the size of the shared memory object
    ftruncate(shm_fd, sizeof(int));

    // memory mapping the shared memory object
    int *count = mmap(0, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (count == MAP_FAILED)
    {
        perror("mmap");
        exit(1);
    }

    *count = 1; // start with 1 for the initial parent process

    a = fork();
    if (a == 0)
    {
        // child process
        (*count)++;
        // printf("New child process created with PID from a: %d\n", getpid());
        create_child_if_odd(getpid(), count);
        exit(0);
    }
    else if (a < 0)
    {
        perror("Fork failed");
        exit(1);
    }

    b = fork();
    if (b == 0)
    {
        // child process
        (*count)++;
        // printf("New child process created with PID from b: %d\n", getpid());
        create_child_if_odd(getpid(), count);
        exit(0);
    }
    else if (b < 0)
    {
        perror("Fork failed");
        exit(1);
    }

    c = fork();
    if (c == 0)
    {
        // child process
        (*count)++;
        // printf("New child process created with PID from c: %d\n", getpid());
        create_child_if_odd(getpid(), count);
        exit(0);
    }
    else if (c < 0)
    {
        perror("Fork failed");
        exit(1);
    }

    // waiting for all child processes to finish
    waitpid(a, NULL, 0);
    waitpid(b, NULL, 0);
    waitpid(c, NULL, 0);

    printf("Total number of processes created: %d\n", *count);

    // cleaning up
    munmap(count, sizeof(int));
    shm_unlink(SHM_NAME);

    return 0;
}