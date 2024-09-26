#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <stdbool.h>

void* block1(void* arg)
{
        for(int i = 1; i <= 5; i++)
        {
                //sleep(1);
                printf("%d. I am Thread-1.\n", i);
        }
        return NULL;
}

void* block2(void* arg)
{
        for(int i = 1; i <= 10; i++)
        {
                //sleep(1);
                printf("%d. I am Thread-2.\n", i);
        }
}

void default_thread()
{
        for(int i = 1; i <= 5; i++)
        {
                sleep(1);
                printf("%d. I am Default Thread.\n", i);
        }
}
//Introduction to thread
int main_1()
{
        pthread_t thread1;
        
        /* Attribute-1: pointer to an unsigned integer value that returns the thread id of the thread created
        Attribute-2: pointer to a structure that is used to define thread attributes like detached state, scheduling policy, stack address, etc. Set to NULL for default thread attributes.
        Attribute-3: pointer to a subroutine that is executed by the thread. The return type and parameter type of the subroutine must be of type void *. The function has a single attribute but if multiple values need to be passed to the function, a struct must be used.
        Attribute-4: pointer to void that contains the arguments to the function defined in the earlier argument
        */
        
        pthread_create(&thread1, NULL, block1, NULL);
        default_thread();
        
        
        /*pthread_join does two things:
        1. Wait for the termination of a thread.
        2. Clean up any resources associated with the thread.
        */
        pthread_join(thread1, NULL);
        
	return 0;
} 

//Introduction to multithread
int main_2()
{
        pthread_t thread1, thread2;
        
        pthread_create(&thread1, NULL, block1, NULL); 
        pthread_create(&thread2, NULL, block2, NULL);
        
        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
        
	return 0;
}


/*===========================================================================================*/

// Creating multiple threads using loop without parallel execution 

int var = 0;
void* block3(void* arg)
{
	var++;
}

int main_3()
{
	pthread_t thread [3];
	for (int i = 0; i < 3; i++)
	{
		pthread_create(&thread[i], NULL, block3, NULL);
		pthread_join(thread[i], NULL);
		printf("Thread: %d has started running.\n", i);
		printf("Thread: %d has ended.\n", i);
	}
		
	printf("The threads have all ended and var is: %d.\n", var);
}


/*===========================================================================================*/


// Creating multiple threads using loop with parallel execution


int main_4()
{
	pthread_t thread [3];
	for (int i = 0; i < 3; i++)
	{
		pthread_create(&thread[i], NULL, block3, NULL);
		printf("Thread: %d has started running.\n", i);
	}
	
	for (int i = 0; i < 3; i++)
	{
		pthread_join(thread[i], NULL);
		printf("Thread: %d has ended.\n", i);
	}
		
	printf("The threads have all ended and var is: %d.\n", var);
}


/*===========================================================================================*/


//Revising processes and child processes
int checker = 0;

int main_5()
{
        int hold = fork(); //Creates a child process and hold = 0 for the child
        
        if(hold == 0)
        {
        	checker++;
                printf("I am the child. My name is %d. My parent is: %d.\n", getpid(), getppid());
                printf("I have been assigned checker no.: %d.\n", checker);
        }
        
        if (hold != 0)
        {
        	printf("I will pause till my child is done.\n");
        	wait(NULL);
                printf("I am the parent. My name is %d.\n", getpid());
                printf("I have been assigned checker no.: %d.\n", checker);
        }
        printf("Final stage: My process ID is: %d.\n", getpid());
        printf("Checker no: %d signing off.\n", checker);
}


/*===========================================================================================*/


//Checking process IDs inside multiple threads
void* block4(void* arg)
{
	printf("This is thread-1. My process ID is: %d.\n", getpid());
}

void* block5(void* arg)
{
	printf("This is thread-2. My process ID is: %d.\n", getpid());
}

int main_6()
{
	pthread_t thread1,  thread2;
	
        pthread_create(&thread1, NULL, block4, NULL); 
        pthread_create(&thread2, NULL, block5, NULL);
        
        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
        
        printf("The threads have exited. The default process ID is: %d.\n", getpid());
        
	return 0;
}


/*===========================================================================================*/


//Checking variables inside multiple threads
int t_checker = 0;

void* block6(void* arg)
{
	t_checker++;
	printf("The value of Thread-1 Checker is: %d.\n", t_checker);
}

void* block7(void* arg)
{
	sleep(1);
	printf("The value of Thread-2 Checker is: %d.\n", t_checker);
}

int main_7()
{
        pthread_t thread1,  thread2;
        
        pthread_create(&thread1, NULL, block6, NULL); 
        pthread_create(&thread2, NULL, block7, NULL);
        
        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
        
	return 0;
}


/*===========================================================================================*/


// Race condition
int racer = 0;

void* block8(void* arg)
{
	//Try with smaller values of i. E.g.: for (int i = 0; i < 100; i++)
	for (int i = 0; i < 1000000000; i++)
	{
		racer++;
	}
}

int main_8()
{
	pthread_t thread1,  thread2;
        
        pthread_create(&thread1, NULL, block8, NULL); 
        pthread_create(&thread2, NULL, block8, NULL);
        
        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
        
        printf("The racer ran: %d miles.\n", racer);
	return 0;
	
	/* Imagine increment happens in 3 stages:
	1. Read and hold value of racer
	2. Increment value of racer
	3. Store the value of racer globally
	
	Sometimes CPU randomly stops a thread and allows some other thread to execute first instead of allowing them to run in parallel. Since, variable values are shared, the other thread might have read and held a value at Step-1 that has long expired. 
	Example: Thread-1 read a value of 100 and OS froze it, Thread-2 runs 2000 times afterwards and new value of racer is 2100, But suddenly OS gives CPU back to Thread-1. Thread-1 will increment 100 by 1 and overwrite racer's value to 101 which is incorrect.*/
}

//Race condition can be solved using mutex


/*===========================================================================================*/


//Passing arguments to threads

int arr [2] = {10, 20};

void* adder(void* arg)
{
	int *index = arg;
	int sum = index[0] + index[1]; 
	printf("I am Thread: 1 performing addition.\n") ;
	sleep(1);
	printf("The sum is: %d.\n", sum);
}

void* subtracter(void* arg)
{
	int *index = arg;
	int diff = index[1] - index[0];  
	printf("I am Thread: 2 performing subtraction.\n"); 
	printf("The difference is: %d.\n", diff);
}


int main_9()
{
	pthread_t thread1, thread2;
	
	pthread_create(&thread1, NULL, adder, (void* )arr);
	pthread_create(&thread2, NULL, subtracter, (void* )arr);

	pthread_join(thread1, NULL);
	pthread_join(thread2, NULL);
}

/*===========================================================================================*/


//Get return value from a thread

void* block9(int *n)
{	
	
	printf("Entered the Thread.\n");
	if(*n % 2 == 0)
	{
		pthread_exit("Odd");
	}
	else
	{
		pthread_exit("Even");
	}
}

int num = 10;
void* thread_return;

int main_10()
{
	pthread_t thread1;
	
	pthread_create(&thread1, NULL, (void*)block9, &num); //try without (void*)
	pthread_join(thread1, &thread_return);
	
	printf("Thread returned: %s\n", (char*)thread_return);
	
	return 0;
}


/*===========================================================================================*/


// Mutex to solve race condition
pthread_mutex_t mut;	//defining a pthread_mutex_t type variable

void* block10(void* arg)
{
	//Try with smaller values of i. E.g.: for (int i = 0; i < 100; i++) 
	for (int i = 0; i < 1000000000; i++)
	{
		//Mutex locking unlocking block protects the code inbetween from being accessed by other threads when a thread is already using it. When the executing thread is done with it, the next thread is allowed to use it.
		pthread_mutex_lock(&mut);
		racer++;
		pthread_mutex_unlock(&mut);
	}
}

int main()
{
	pthread_t thread [4];
	pthread_mutex_init(&mut, NULL);	//for first argument pass address of the mutex, and leave the other one to NULL (default)
	
	for (int i = 0; i < 4; i++)
	{
		pthread_create(&thread[i], NULL, block10, NULL);
		printf("Thread: %d has started running.\n", i);
	}
	
	for (int i = 0; i < 4; i++)
	{
		pthread_join(thread[i], NULL);
		printf("Thread: %d has ended.\n", i);
	}
	pthread_mutex_destroy(&mut);
		
	printf("The racer ran: %d miles.\n", racer);
	return 0;
}


/*===========================================================================================*/



// Introduction to semaphore

#include <semaphore.h>
sem_t semaphore;	//defining a sem_t type variable //semaphores are integers
int thread_ids[4] = {0, 1, 2, 3};

void* block11(void* arg)
{
	//sem_wait checks if the value of the semaphore variable is 0 or not. If 0, it can no longer be decremented, sem_wait will make a thread/s wait from executing until semaphore > 0. If semaphore > 0, sem_wait first decrements value of semaphore by 1 for each thread, and then allow thread/s to continue execution until semaphore == 0. The selection of waiting threads that will be alllowed to execute once semaphore > 0 is random.
	sem_wait(&semaphore);
	sleep(1);
	printf("Thread-%d is busy sleeping. Others, please wait.\n", *(int*)arg);
	sleep(5);
	printf("Thread-%d is awake now.\n", *(int*)arg);
	//sem_post increments the value of semaphore variable by 1
	sem_post(&semaphore);
}

int main_12()
{
	pthread_t thread [4];
	
	//for first argument pass address of the semaphore variable created above, the second argument is the number of processes that are running (0 if only the main process is running), the third parameter is the initial value of the semaphore (it denotes how many threads will be running at a time.)
	sem_init(&semaphore, 0, 1);	
	
	for (int i = 0; i < 4; i++)
	{
		pthread_create(&thread[i], NULL, block11, &thread_ids[i]);
		printf("Thread: %d has started running.\n", i);
	}
	
	for (int i = 0; i < 4; i++)
	{
		pthread_join(thread[i], NULL);
		//printf("Thread: %d has ended.\n", i);
	}
	sem_destroy(&semaphore);
		
	printf("The threads have all ended.\n");
	return 0;
}


/*===========================================================================================*/



// Using semaphores like mutexes

int advised = 0;

void* block12(void* arg)
{
	sleep(1);
	sem_wait(&semaphore);
	printf("Year-%d students are now advising. Others, please wait.\n", *(int*)arg + 1);
	
	for (int i = 0; i < 100; i++)
	{
		advised++;
	}
	
	sleep(10);
	printf("Total students advised: %d.\n", advised);
	sem_post(&semaphore);
	
}

int main_13()
{
	pthread_t thread [4];
	
	//for first argument pass address of the semaphore variable created above, the second argument is the number of processes that are running (0 if only the main process is running), the third parameter is the initial value of the semaphore (it denotes how many threads will be running at a time.)
	sem_init(&semaphore, 0, 2);	
	
	for (int i = 0; i < 4; i++)
	{
		pthread_create(&thread[i], NULL, block12, &thread_ids[i]);
		printf("Thread: %d has started running.\n", i);
	}
	
	for (int i = 0; i < 4; i++)
	{
		pthread_join(thread[i], NULL);
		//printf("Thread: %d has ended.\n", i);
	}
	sem_destroy(&semaphore);
		
	printf("All students have completed their advising.\n");
	return 0;
}



