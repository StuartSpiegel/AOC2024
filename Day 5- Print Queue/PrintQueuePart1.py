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

def main():
    rules, updates = read_input('input.txt')
    sum_of_middle_pages = 0

    for i, update in enumerate(updates):
        if is_order_valid(update, rules):
            middle_index = len(update) // 2
            middle_page = update[middle_index]
            sum_of_middle_pages += middle_page
            print(f"Update {i + 1} is in correct order. Middle page: {middle_page}")
        else:
            print(f"Update {i + 1} is NOT in correct order.")

    print(f"Sum of middle pages: {sum_of_middle_pages}")

if __name__ == "__main__":
    main()
