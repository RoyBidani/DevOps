#include <stdio.h>

int josephus(int n, int k) {
    int soldiers[n];
    int i, alive, count;

    // Initializing soldiers with the value 1 which means they are alived
    for (i = 0; i < n; i++) {
        soldiers[i] = 1;
    }

    // Eliminating soldiers until only one is left
    i = 0;
    alive = n;
    count = 0;
    while (alive > 1) {
        if (soldiers[i] == 1) {
            count++;
            if (count == k) {
                soldiers[i] = 0;
                count = 0;
                alive--;
            }
        }
        i = (i + 1) % n;
    }

    // Finding the index of the last soldier standing
    for (i = 0; i < n; i++) {
        if (soldiers[i] == 1) {
            return i;
        }
    }

    return -1;  // Error condition
}

int main() {
    int n = 100;  // Number of soldiers
    int k = 1;    // Step size

    int lastSoldier = josephus(n, k);
    printf("Index of the last soldier standing: %d\n", lastSoldier);

    return 0;
}

