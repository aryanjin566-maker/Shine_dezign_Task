my_list=[]

while True:
    
    print("MENU")
    print("1. create (Add element to the list)")
    print("2. read (Display the list)")
    print("3. update (Modify an element in the list)")
    print("4. delete (Remove an element from the list)")
    print("5. Exit")

    # Input
    choice = int(input("Enter your choice : "))

    if choice == 1 : #add element to the list
        element = input("Enter the element to add: ")
        my_list.append(element)
        print(f"'{element}' added to the list.")

    elif choice == 2 : #display the list
        if len(my_list) == 0 :
            print("The list is empty.")
        else:
            print ("current list: " , my_list)
    
    elif choice == 3 : #modify an element in the list
          if len(my_list) == 0 :
            print("The list is empty.")
          else:
              print("current list: " , my_list)
              index = int(input("Enter the index of the element to update: "))
              if 0 <= index < len(my_list):
                  new_element = input("Enter the new element: ")
                  my_list[index] = new_element
                  print(f"Element at index {index} updated to '{new_element}'.")
              else:
                  print("Invalid index.")
    
    elif choice == 4 : #remove an element from the list
          if len(my_list)== 0 :
            print("The list is empty.")
          else:
              print("current list: " , my_list)
              index = int(input("Enter the index of the element to delete: "))
              if 0 <= index < len(my_list):
                  removed_element = my_list.pop(index)
                  print(f"Element '{removed_element}' at index {index} removed from the list.")
              else:
                  print("Invalid index.")

    elif choice == 5 : #exit
        print("Exiting the program.")
        break           
    else:
        print("Invalid choice. Please try again.")
