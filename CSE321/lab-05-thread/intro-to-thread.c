#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

void *funcThread(void *arg);

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, funcThread, NULL);
    func1();
}