#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

struct my_msg
{
    long int type;
    char txt[10]; // Increased size to accommodate "cse321"
};

int main()
{
    int msgid;
    key_t key = 1234;
    struct my_msg message;
    pid_t pid_otp, pid_mail;

    // Create message queue
    msgid = msgget(key, IPC_CREAT | 0666);
    if (msgid < 0)
    {
        perror("msgget");
        exit(1);
    }

    // Log in process
    printf("Please enter the workspace name:\n");
    char workspace[10];
    scanf("%s", workspace);

    if (strcmp(workspace, "cse321") != 0)
    {
        printf("Invalid workspace name\n");
        msgctl(msgid, IPC_RMID, NULL); // Remove message queue
        exit(1);
    }

    // Write workspace name to message queue
    message.type = 1;
    strcpy(message.txt, "cse321");
    msgsnd(msgid, &message, sizeof(message.txt), 0);
    printf("Workspace name sent to otp generator from log in: %s\n", message.txt);

    // Fork OTP generator process
    pid_otp = fork();
    if (pid_otp < 0)
    {
        perror("fork");
        exit(1);
    }
    else if (pid_otp == 0)
    { // OTP generator process
        msgrcv(msgid, &message, sizeof(message.txt), 1, 0);
        printf("OTP generator received workspace name from log in: %s\n", message.txt);

        // Generate OTP
        int otp = getpid();
        snprintf(message.txt, sizeof(message.txt), "%d", otp);
        message.type = 2;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to log in from OTP generator: %s\n", message.txt);

        // Send OTP to mail process
        message.type = 3;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to mail from OTP generator: %s\n", message.txt);

        // Fork mail process
        pid_mail = fork();
        if (pid_mail < 0)
        {
            perror("fork");
            exit(1);
        }
        else if (pid_mail == 0)
        { // Mail process
            msgrcv(msgid, &message, sizeof(message.txt), 3, 0);
            printf("Mail received OTP from OTP generator: %s\n", message.txt);

            // Send OTP to log in process
            message.type = 4;
            msgsnd(msgid, &message, sizeof(message.txt), 0);
            printf("OTP sent to log in from mail: %s\n", message.txt);

            exit(0);
        }
        else
        {
            wait(NULL); // Wait for mail process to finish
            exit(0);
        }
    }
    else
    {
        wait(NULL); // Wait for OTP generator process to finish

        // Read OTP from OTP generator
        msgrcv(msgid, &message, sizeof(message.txt), 2, 0);
        printf("Log in received OTP from OTP generator: %s\n", message.txt);
        char otp_from_otp[10];
        strcpy(otp_from_otp, message.txt);

        // Read OTP from mail
        msgrcv(msgid, &message, sizeof(message.txt), 4, 0);
        printf("Log in received OTP from mail: %s\n", message.txt);
        char otp_from_mail[10];
        strcpy(otp_from_mail, message.txt);

        // Compare OTPs
        if (strcmp(otp_from_otp, otp_from_mail) == 0)
        {
            printf("OTP Verified\n");
        }
        else
        {
            printf("OTP Incorrect\n");
        }

        // Remove message queue
        msgctl(msgid, IPC_RMID, NULL);
    }

    return 0;
}