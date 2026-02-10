

# Inventory dictionary
inventory = {}

while True:
    print("\n1. Add Item / Add Quantity")
    print("2. Remove Quantity")
    print("3. Delete Item")
    print("4. View Inventory")
    print("5. Exit")
  
    choice = int(input("Enter your choice: "))

    if choice == 1:
      item_name = input("Enter item name: ")
      quantity = int(input("Enter quantity: "))
      if item_name in inventory:
        inventory[item_name] += quantity
        print("Item quantity updated.")
      else:
        inventory[item_name] = quantity
        print("Item added to inventory.")

    elif choice == 2:
            item = input("Enter item name: ")
            if item in inventory:
                qty = int(input("Enter quantity to remove: "))
                if qty <= inventory[item]:
                    inventory[item] = inventory[item] - qty
                    print("Quantity removed")

                    if inventory[item] == 0:        
                     print("Inventory is Empty Now")  
            else:
                print("Item not found")

    elif choice == 3:
        item = input("Enter item name to delete: ")
        if item in inventory:
                del inventory[item]
                print("Item deleted")
        else:
                print("Item not found")
    elif choice == 4:
         print("Inventory:", inventory)

    elif choice == 5:
        print("Exiting program")
        break
    else:
        print("Invalid choice. Please try again.")

    
        