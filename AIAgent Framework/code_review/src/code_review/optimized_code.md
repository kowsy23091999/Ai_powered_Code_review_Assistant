Here is a cleaner, optimized version of the provided code, preserving the original functionality while improving for performance, readability, robustness, and adding input validation and error handling:

```python
# Optimized Inventory Management System

inventory = {}


def add_item(name, quantity, price):
    """
    Add an item to the inventory or update its quantity if it already exists.
    
    :param name: Name of the item
    :param quantity: Quantity of the item to add
    :param price: Price of the item
    """
    if name in inventory:
        inventory[name]['quantity'] += quantity
    else:
        inventory[name] = {'quantity': quantity, 'price': price}


def remove_item(name, quantity):
    """
    Remove a certain quantity of an item from the inventory.
    If the quantity is zero after removal, delete the item from the inventory.
    
    :param name: Name of the item
    :param quantity: Quantity of the item to remove
    """
    if name in inventory:
        if inventory[name]['quantity'] >= quantity:
            inventory[name]['quantity'] -= quantity
            if inventory[name]['quantity'] == 0:
                del inventory[name]
        else:
            print(f"Error: Not enough {name} in inventory to remove {quantity}.")
    else:
        print(f"Error: {name} not found in inventory.")


def update_price(name, price):
    """
    Update the price of an item in the inventory.
    
    :param name: Name of the item
    :param price: New price of the item
    """
    if name in inventory:
        inventory[name]['price'] = price
    else:
        print(f"Error: {name} not found in inventory.")


def get_inventory():
    """
    Return the current inventory.
    
    :return: Dictionary representing the inventory
    """
    return inventory


def display_inventory():
    """
    Print the current inventory.
    """
    for name, data in inventory.items():
        print(f"Item: {name}, Quantity: {data['quantity']}, Price: {data['price']}")


def safe_input(prompt, type_func):
    """
    Safely capture user input and validate against the required type.
    
    :param prompt: Text to display to the user
    :param type_func: Expected type of the input
    :return: User input converted to the appropriate type
    """
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")


def handle_add_item():
    """
    Handle adding an item to the inventory through user prompts.
    """
    name = input("Enter the name of the item: ")
    quantity = safe_input("Enter the quantity of the item: ", int)
    price = safe_input("Enter the price of the item: ", float)
    add_item(name, quantity, price)


def handle_remove_item():
    """
    Handle removing an item from the inventory through user prompts.
    """
    name = input("Enter the name of the item: ")
    quantity = safe_input("Enter the quantity of the item to remove: ", int)
    remove_item(name, quantity)


def handle_update_price():
    """
    Handle updating the price of an item in the inventory through user prompts.
    """
    name = input("Enter the name of the item: ")
    price = safe_input("Enter the new price of the item: ", float)
    update_price(name, price)


def main():
    """
    Main function to run the inventory management system.
    """
    actions = {
        '1': handle_add_item,
        '2': handle_remove_item,
        '3': handle_update_price,
        '4': display_inventory,
    }

    while True:
        print("1. Add item")
        print("2. Remove item")
        print("3. Update price")
        print("4. Display inventory")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice in actions:
            actions[choice]()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
```

With these improvements, the script:

- Ensures proper input validation through the `safe_input` function
- Maps user choices to handler functions using a dictionary for better readability and maintainability
- Includes proper error messages and handling scenarios where the requested item or quantity is not available
- Preserves the original functionality while making the codebase cleaner and more robust