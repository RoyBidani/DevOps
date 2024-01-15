#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

extern char **environ;

char** copyLowerCaseEnvironment() {
    // Counting the number of environment variables
    int count = 0;
    char **env = environ;
    while (*env != NULL) {
        count++;
        env++;
    }

    // Allocating memory for the new buffer
    char **envLower = (char **)malloc((count + 1) * sizeof(char *));
    if (envLower == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    // Copying environment variables into the new buffer in lowercase
    env = environ;
    int i = 0;
    while (*env != NULL) {
        char *variable = *env;
        int length = strlen(variable);
        char *lower = (char *)malloc((length + 1) * sizeof(char));
        if (lower == NULL) {
            printf("Memory allocation failed.\n");
            return NULL;
        }

        // Converting to lowercase
        for (int j = 0; j < length; j++) {
            lower[j] = tolower(variable[j]);
        }
        lower[length] = '\0';

        // Storing the lowercase variable in the new buffer
        envLower[i] = lower;

        env++;
        i++;
    }
    envLower[i] = NULL;  // Marking the end of the buffer with a NULL pointer

    return envLower;
}

void printLowerCaseEnvironment(char **envLower) {
    if (envLower == NULL) {
        return;
    }

    // Printing the lowercase environment variables
    int i = 0;
    while (envLower[i] != NULL) {
        printf("%s\n", envLower[i]);
        i++;
    }
}

int main() {
    char **envLower = copyLowerCaseEnvironment();
    printLowerCaseEnvironment(envLower);

    // Freeing the allocated memory
    if (envLower != NULL) {
        int i = 0;
        while (envLower[i] != NULL) {
            free(envLower[i]);
            i++;
        }
        free(envLower);
    }

    return 0;
}
