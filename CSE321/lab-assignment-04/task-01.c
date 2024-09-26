#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MAX 10 // producers and consumers can produce and consume upto MAX
#define BUFLEN 7
#define NUMTHREAD 2 /* number of threads */

void *consumer(int *id);
void *producer(int *id);

char buffer[BUFLEN];
char source[BUFLEN]; // from this array producer will store it's production into buffer
int pCount = 0;
int cCount = 0;
int buflen;
int in = 0;
int out = 0;

// initializing pthread mutex and condition variables
pthread_mutex_t count_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t nonEmpty = PTHREAD_COND_INITIALIZER;
pthread_cond_t full = PTHREAD_COND_INITIALIZER;
int thread_id[NUMTHREAD] = {0, 1};

int main()
{
    pthread_t thread[NUMTHREAD];

    strcpy(source, "abcdef");
    buflen = strlen(source);

    pthread_create(&thread[0], NULL, (void *)producer, &thread_id[0]);
    pthread_create(&thread[1], NULL, (void *)consumer, &thread_id[1]);

    pthread_join(thread[0], NULL);
    pthread_join(thread[1], NULL);

    return 0;
}

void *producer(int *id)
{
    while (pCount < MAX)
    {
        pthread_mutex_lock(&count_mutex);

        while ((in + 1) % BUFLEN == out)
        {
            pthread_cond_wait(&full, &count_mutex);
        }

        buffer[in] = source[in % buflen];
        printf("%d produced  %c  by Thread  %d\n", pCount, buffer[in], *id);
        in = (in + 1) % BUFLEN;
        pCount++;

        pthread_cond_signal(&nonEmpty);
        pthread_mutex_unlock(&count_mutex);

        sleep(1); // Slow down the producer
    }
    return NULL;
}

void *consumer(int *id)
{
    while (cCount < MAX)
    {
        pthread_mutex_lock(&count_mutex);

        while (in == out)
        {
            pthread_cond_wait(&nonEmpty, &count_mutex);
        }

        char item = buffer[out];
        printf("%d consumed  %c  by Thread  %d\n", cCount, item, *id);
        out = (out + 1) % BUFLEN;
        cCount++;

        pthread_cond_signal(&full);
        pthread_mutex_unlock(&count_mutex);

        sleep(2); // Slow down the consumer
    }
    return NULL;
}