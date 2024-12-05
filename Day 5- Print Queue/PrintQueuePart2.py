from collections import defaultdict

def read_input(file_name):
    rules = []
    updates = []
    reading_rules = True
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                reading_rules = False
                continue

            if reading_rules:
                before, after = map(int, line.split('|'))
                rules.append((before, after))
            else:
                updates.append(list(map(int, line.split(','))))
    return rules, updates

def is_order_valid(update, rules):
    positions = {page: index for index, page in enumerate(update)}
    for before, after in rules:
        if before in positions and after in positions:
            if positions[before] > positions[after]:
                return False
    return True

def correct_order(update, rules):
    dependency_graph = defaultdict(set)
    indegree = defaultdict(int)
    pages = set(update)

    for before, after in rules:
        if before in pages and after in pages:
            dependency_graph[before].add(after)
            indegree[after] += 1

    # Topological sort to determine the correct order
    sorted_pages = []
    zero_indegree = [page for page in update if indegree[page] == 0]

    while zero_indegree:
        current = zero_indegree.pop()
        sorted_pages.append(current)
        for neighbor in dependency_graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_indegree.append(neighbor)

    return sorted_pages

def main():
    rules, updates = read_input('input.txt')
    sum_of_middle_pages_correct = 0
    sum_of_middle_pages_fixed = 0

    for i, update in enumerate(updates):
        if is_order_valid(update, rules):
            middle_index = len(update) // 2
            middle_page = update[middle_index]
            sum_of_middle_pages_correct += middle_page
            print(f"Update {i + 1} is in correct order. Middle page: {middle_page}")
        else:
            print(f"Update {i + 1} is NOT in correct order.")
            corrected_update = correct_order(update, rules)
            middle_index = len(corrected_update) // 2
            middle_page = corrected_update[middle_index]
            sum_of_middle_pages_fixed += middle_page
            print(f"Corrected Update {i + 1}: {corrected_update}. Middle page after correction: {middle_page}")

    print(f"Sum of middle pages of correctly ordered updates: {sum_of_middle_pages_correct}")
    print(f"Sum of middle pages after correcting unordered updates: {sum_of_middle_pages_fixed}")

if __name__ == "__main__":
    main()
