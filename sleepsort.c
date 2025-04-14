#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

void *sleepPrint(void *ptr) {
    int num = *(int *)ptr;
    // sleep for num seconds, then print num
    sleep(num);
    printf("%d\n", num);

    pthread_exit(NULL);
}

int main() {
    // generate 100 random ints from 0 to 99 inclusive
    int nums[100];
    // the memory address returned by the kernel is the random seed (this works because of ASLR)
    srand((long)malloc(1));
    for (int i = 0; i < 100; i++)
        nums[i] = random() % 100;

    pthread_t threads[100];

    // generate a hundred threads
    for (int i = 0; i < 100; i++) 
        pthread_create(&threads[i], NULL, sleepPrint, (void*) &nums[i]);

    // wait for them to finish before exiting
    for (int i = 0; i < 100; i++)
        pthread_join(threads[i], NULL);

    return 0;
}
