def confirm_action(prompt="Are you sure? (y/n): "):
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter y/yes or n/no.")
