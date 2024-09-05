#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* threadFunction(void* arg) {
    int thread_num = *((int*)arg);
    printf("thread-%d running\n", thread_num);
    // sleep for 1s
    sleep(1);
    printf("thread-%d closed\n", thread_num);
    // sleep for 500ms
    usleep(500000);
    return NULL;
}

int main() {
    pthread_t threads[5];
    int thread_nums[5];

    for (int i = 0; i < 5; i++) {
        thread_nums[i] = i + 1;
        pthread_create(&threads[i], NULL, threadFunction, &thread_nums[i]);
        pthread_join(threads[i], NULL);
    }

    return 0;
}