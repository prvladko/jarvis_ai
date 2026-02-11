# Create a simple list application in Python

def main():
    # Initialize an empty list
    my_list = []

    while True:
        print("\nOptions:")
        print("1. Add item to the list")
        print("2. Remove item from the list")
        print("3. Display items in the list")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            item = input("Enter the item to add: ")
            my_list.append(item)
            print(f"{item} added to the list.")
        elif choice == '2':
            item = input("Enter the item to remove: ")
            if item in my_list:
                my_list.remove(item)
                print(f"{item} removed from the list.")
            else:
                print(f"{item} not found in the list.")
        elif choice == '3':
            print("Items in the list:")
            for index, item in enumerate(my_list, 1):
                print(f"{index}. {item}")
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()