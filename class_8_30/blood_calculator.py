def interface():
    print("Blood calculator")
    keep_running = True
    while keep_running:
        print("Make a choice")
        print("9 - Quit")
        choice = int(input("Enter your choice:"))
        if choice == 9:
	    keep_running = False
            return
   print(choice)
   return choice


interface()
