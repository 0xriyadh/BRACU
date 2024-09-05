#include <pthread.h>
#include <stdio.h>
#include <string.h>

struct ThreadData
{
    char *username;
    int result;
};

void *calculateAsciiSum(void *arg)
{
    struct ThreadData *data = (struct ThreadData *)arg; // typecasting void* to struct ThreadData*
    int sum = 0;
    for (int i = 0; i < strlen(data->username); i++)
    {
        sum += data->username[i];
    }
    data->result = sum;
    return NULL;
}

void *compareResults(void *arg)
{
    struct ThreadData *data = (struct ThreadData *)arg;
    int result1 = data[0].result;
    int result2 = data[1].result;
    int result3 = data[2].result;

    if (result1 == result2 && result2 == result3)
    {
        printf("Youreka\n");
    }
    else if (result1 == result2 || result2 == result3 || result1 == result3)
    {
        printf("Miracle\n");
    }
    else
    {
        printf("Hasta la vista\n");
    }
    return NULL;
}

int main()
{
    pthread_t threads[3];
    pthread_t compareThread;
    struct ThreadData threadData[3] = {
        {"Siam", 0},
        {"Nafis", 0},
        {"Mahim", 0}};

    for (int i = 0; i < 3; i++)
    {
        pthread_create(&threads[i], NULL, calculateAsciiSum, &threadData[i]);
    }

    for (int i = 0; i < 3; i++)
    {
        pthread_join(threads[i], NULL);
    }

    pthread_create(&compareThread, NULL, compareResults, threadData);

    pthread_join(compareThread, NULL);

    return 0;
}