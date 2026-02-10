inventory = {}

while True:
    print("\n1. Add Item / Add Quantity")
    print("2. Remove Quantity")
    print("3. Delete Item")
    print("4. View Inventory")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    match choice:

        # Add item OR add quantity
        case 1:
            item = input("Enter item name: ")
            qty = int(input("Enter quantity to add: "))

            if item in inventory:
                inventory[item] = inventory[item] + qty
                print("Quantity added to existing item")
            else:
                inventory[item] = qty
                print("New item added")

        # Remove quantity
        case 2:
            item = input("Enter item name: ")
            if item in inventory:
                qty = int(input("Enter quantity to remove: "))
                if qty <= inventory[item]:
                    inventory[item] = inventory[item] - qty
                    print("Quantity removed")

                    if inventory[item] == 0:
                        del inventory[item]
                        print("Item removed as quantity is zero")
                else:
                    print("Not enough stock")
            else:
                print("Item not found")

        # Delete item completely
        case 3:
            item = input("Enter item name to delete: ")
            if item in inventory:
                del inventory[item]
                print("Item deleted")
            else:
                print("Item not found")

        # View inventory
        case 4:
            print("Inventory:", inventory)

        # Exit
        case 5:
            print("Exiting program")
            break

        case _:
            print("Invalid choice")
