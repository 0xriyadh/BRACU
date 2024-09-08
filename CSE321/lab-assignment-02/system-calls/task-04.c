#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/mman.h>

int compare(const void *a, const void *b)
{
    return (*(int *)b - *(int *)a);
}

void sortArray(int arr[], int n)
{
    qsort(arr, n, sizeof(int), compare);
}

void printOddEvenStatus(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        if (arr[i] % 2 == 0)
        {
            printf("%d is even\n", arr[i]);
        }
        else
        {
            printf("%d is odd\n", arr[i]);
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: %s <numbers>\n", argv[0]);
        return 1;
    }

    int n = argc - 1;

    // Create shared memory for the array
    int *arr = mmap(NULL, n * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (arr == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }

    for (int i = 0; i < n; i++)
    {
        arr[i] = atoi(argv[i + 1]);
    }

    pid_t pid = fork();

    if (pid < 0)
    {
        perror("fork");
        return 1;
    }
    else if (pid == 0)
    {
        // Child process: Sort the array
        sortArray(arr, n);
        printf("Sorted array in descending order: ");
        for (int i = 0; i < n; i++)
        {
            printf("%d ", arr[i]);
        }
        printf("\n");
        exit(0);
    }
    else
    {
        // Parent process: Wait for the child to finish
        wait(NULL);
        // Print odd/even status for the sorted array
        printOddEvenStatus(arr, n);
    }

    // Unmap shared memory
    munmap(arr, n * sizeof(int));

    return 0;
}