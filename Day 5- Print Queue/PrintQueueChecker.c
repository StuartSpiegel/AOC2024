#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_RULES 1000
#define MAX_UPDATES 1000
#define MAX_PAGES 500

typedef struct {
    int before;
    int after;
} Rule;

Rule rules[MAX_RULES];
int num_rules = 0;

int updates[MAX_UPDATES][MAX_PAGES];
int update_lengths[MAX_UPDATES];
int num_updates = 0;

void add_rule(int before, int after) {
    rules[num_rules].before = before;
    rules[num_rules].after = after;
    num_rules++;
}

void add_update(int *pages, int length) {
    for (int i = 0; i < length; i++) {
        updates[num_updates][i] = pages[i];
    }
    update_lengths[num_updates] = length;
    num_updates++;
}

bool is_order_valid(int *pages, int length) {
    // Create a hash map-like array to track the position of each page in the current update
    int positions[10000]; // Assuming page numbers are less than 10000
    for (int i = 0; i < 10000; i++) {
        positions[i] = -1;
    }

    // Set positions for current update
    for (int i = 0; i < length; i++) {
        positions[pages[i]] = i;
    }

    bool valid = true;

    // Validate all rules for the current update
    for (int i = 0; i < num_rules; i++) {
        int before = rules[i].before;
        int after = rules[i].after;

        // Check if both pages are in the current update
        if (positions[before] != -1 && positions[after] != -1) {
            if (positions[before] > positions[after]) {
                // Debug output to identify which rule fails
                printf("Rule violated: %d must be before %d in update (Position %d vs %d)\n", before, after, positions[before], positions[after]);
                valid = false;
            }
        }
    }
    return valid;
}

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Error: could not open input file\n");
        return 1;
    }

    // Read rules from file
    char line[256];
    bool reading_rules = true;
    while (fgets(line, sizeof(line), file)) {
        // Remove newline character
        line[strcspn(line, "\n")] = 0;

        if (strlen(line) == 0) {
            // Empty line indicates the end of rules section
            reading_rules = false;
            continue;
        }

        if (reading_rules) {
            int before, after;
            if (sscanf(line, "%d|%d", &before, &after) == 2) {
                add_rule(before, after);
            }
        } else {
            int pages[MAX_PAGES];
            int length = 0;
            char *token = strtok(line, ",");
            while (token != NULL) {
                pages[length++] = atoi(token);
                token = strtok(NULL, ",");
            }
            if (length > 0) {
                add_update(pages, length);
            }
        }
    }

    fclose(file);

    long long sum_of_middle_pages = 0;

    for (int i = 0; i < num_updates; i++) {
        bool valid = is_order_valid(updates[i], update_lengths[i]);
        if (valid) {
            int middle_page = 0;
            if (update_lengths[i] % 2 == 0) {
                // Take average of two middle pages for even length updates
                int middle_index_1 = (update_lengths[i] / 2) - 1;
                int middle_index_2 = update_lengths[i] / 2;
                middle_page = (updates[i][middle_index_1] + updates[i][middle_index_2]) / 2;
            } else {
                // Take the middle page for odd length updates
                int middle_index = update_lengths[i] / 2;
                middle_page = updates[i][middle_index];
            }

            sum_of_middle_pages += (long long)middle_page;
            printf("Update %d is in correct order. Middle page: %d\n", i + 1, middle_page);
        } else {
            printf("Update %d is NOT in correct order.\n", i + 1);
        }
    }

    printf("Sum of middle pages: %lld\n", sum_of_middle_pages);

    return 0;
}
