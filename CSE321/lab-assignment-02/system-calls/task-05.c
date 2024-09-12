#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid, grandchild_pid;

    // Parent process
    printf("Parent process ID: %d\n", getpid());

    // Create one child process
    pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child process
        printf("Child process ID: %d\n", getpid());

        // Create three grandchild processes
        for (int i = 0; i < 3; i++) {
            grandchild_pid = fork();

            if (grandchild_pid < 0) {
                perror("fork");
                return 1;
            } else if (grandchild_pid == 0) {
                // Grandchild process
                printf("Grandchild process ID: %d\n", getpid());
                exit(0); // Grandchild process exits
            } else {
                // Child process waits for each grandchild to finish
                wait(NULL);
            }
        }
        exit(0); // Child process exits after creating grandchildren
    } else {
        // Parent process waits for the child to finish
        wait(NULL);
    }

    return 0;
}