#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>

struct shared
{
    char sel[100];
    int b;
};

int main()
{
    int fd[2];
    pid_t a;
    char pipe_buff[200];
    int shmid;
    key_t key = 1234;
    struct shared *shm;

    // Create shared memory
    shmid = shmget(key, sizeof(struct shared), IPC_CREAT | 0666);
    if (shmid < 0)
    {
        perror("shmget");
        exit(1);
    }

    // Attach shared memory
    shm = (struct shared *)shmat(shmid, NULL, 0);
    if (shm == (struct shared *)-1)
    {
        perror("shmat");
        exit(1);
    }

    // Initialize shared memory
    shm->b = 1000;

    // Create pipe
    if (pipe(fd) == -1)
    {
        perror("pipe");
        exit(1);
    }

    a = fork();
    if (a < 0)
    {
        perror("fork");
        exit(1);
    }
    else if (a == 0)
    { // Child process
        close(fd[0]);

        // Read user input
        printf("Provide Your Input From Given Options:\n");
        printf("1. Type a to Add Money\n");
        printf("2. Type w to Withdraw Money\n");
        printf("3. Type c to Check Balance\n");
        read(0, shm->sel, sizeof(shm->sel));
        shm->sel[strcspn(shm->sel, "\n")] = 0; // Remove newline character
        printf("Your selection: %s\n", shm->sel);

        // Perform operations based on user input
        if (strcmp(shm->sel, "a") == 0)
        {
            int amount;
            printf("Enter amount to be added:\n");
            scanf("%d", &amount);
            if (amount > 0)
            {
                shm->b += amount;
                printf("Balance added successfully\n");
                printf("Updated balance after addition: %d\n", shm->b);
            }
            else
            {
                printf("Adding failed, Invalid amount\n");
            }
        }
        else if (strcmp(shm->sel, "w") == 0)
        {
            int amount;
            printf("Enter amount to be withdrawn:\n");
            scanf("%d", &amount);
            if (amount > 0 && amount <= shm->b)
            {
                shm->b -= amount;
                printf("Balance withdrawn successfully\n");
                printf("Updated balance after withdrawal: %d\n", shm->b);
            }
            else
            {
                printf("Withdrawal failed, Invalid amount\n");
            }
        }
        else if (strcmp(shm->sel, "c") == 0)
        {
            printf("Your current balance is: %d\n", shm->b);
        }
        else
        {
            printf("Invalid selection\n");
        }

        // Write thank you message to pipe
        strcpy(pipe_buff, "Thank you for using");
        write(fd[1], pipe_buff, sizeof(pipe_buff));
        close(fd[1]);

        // Detach and remove shared memory
        shmdt((void *)shm);
        shmctl(shmid, IPC_RMID, NULL);

        exit(0);
    }
    else
    { // Parent process
        wait(NULL);
        close(fd[1]);

        // Read thank you message from pipe
        read(fd[0], pipe_buff, sizeof(pipe_buff));
        printf("%s\n", pipe_buff);
        close(fd[0]);

        // Detach shared memory
        shmdt((void *)shm);
    }

    return 0;
}