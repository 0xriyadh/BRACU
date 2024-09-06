#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int process_count = 1; // Start with the initial parent process

void create_additional_child_if_odd(pid_t pid) {
    if (pid > 0 && pid % 2 != 0) { // Check if PID is odd
        pid_t new_pid = fork();
        if (new_pid == 0) {
            // New child process
            process_count++;
        } else if (new_pid > 0) {
            // Parent process
            wait(NULL); // Waiting for the new child to finish
        }
    }
}

int main() {
    pid_t a, b, c;

    a = fork();
    if (a == 0) {
        // Child process
        process_count++;
    } else if (a > 0) {
        wait(NULL); // Waiting for the child process to finish
    }

    b = fork();
    if (b == 0) {
        // Child process
        process_count++;
    } else if (b > 0) {
        wait(NULL); // Waiting for the child process to finish
    }

    c = fork();
    if (c == 0) {
        // Child process
        process_count++;
    } else if (c > 0) {
        wait(NULL); // Wait for the child process to finish
    }

    // Check and create additional child processes if PID is odd
    if (a > 0 && b > 0 && c > 0) { // Ensure this is the original parent process
        wait(NULL); // Wait for the child process to finish
        create_additional_child_if_odd(a);
        create_additional_child_if_odd(b);
        create_additional_child_if_odd(c);
        wait(NULL); // Wait for the last child process to finish
        printf("Total number of processes created: %d\n", process_count);
    }

    // Print the total number of processes created
    // if (a > 0 && b > 0 && c > 0) { // Ensure this is the original parent process
    //     printf("Total number of processes created: %d\n", process_count);
    // }

    return 0;
}