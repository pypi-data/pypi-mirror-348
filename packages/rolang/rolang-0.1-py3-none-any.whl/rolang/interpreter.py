def run_rolang(code):
    if code.startswith("bolo"):
        message = code[5:].strip('" ')
        print(message)

    elif code.startswith("jod") or code.startswith("plus"):
        try:
            parts = code.split()
            x = int(parts[1])
            y = int(parts[3])
            print(x + y)
        except:
            print("⚠️ Error in addition syntax. Use: jod 5 aur 3")

    elif code.startswith("ghata") or code.startswith("minus"):
        try:
            parts = code.split()
            x = int(parts[1])
            y = int(parts[3])
            print(x - y)
        except:
            print("⚠️ Error in subtraction syntax. Use: ghata 10 aur 4")

    elif code.startswith("guna") or code.startswith("multiply"):
        try:
            parts = code.split()
            x = int(parts[1])
            y = int(parts[3])
            print(x * y)
        except:
            print("⚠️ Error in multiplication syntax. Use: guna 5 aur 3")

    elif code.startswith("bhaag") or code.startswith("divide"):
        try:
            parts = code.split()
            x = int(parts[1])
            y = int(parts[3])
            if y == 0:
                print("⚠️ Division by zero error!")
            else:
                print(x / y)
        except:
            print("⚠️ Error in division syntax. Use: bhaag 10 aur 2")

    elif code.startswith("agar"):
        try:
            condition_part, action_part = code.split("toh")
            condition_part = condition_part.strip()[5:]  # Remove 'agar '
            x, op, y = condition_part.strip().split()
            x = int(x)
            y = int(y)
            condition_met = False

            if op == ">":
                condition_met = x > y
            elif op == "<":
                condition_met = x < y
            elif op == "==":
                condition_met = x == y

            if condition_met and "bolo" in action_part:
                message = action_part.strip()[5:].strip('" ')
                print(message)
        except:
            print("⚠️ Error in agar syntax. Use: agar 5 > 2 toh bolo \"message\"")

    elif code.startswith("repeat"):
        try:
            parts = code.split("baar")
            count_part = parts[0].strip()  # e.g. 'repeat 3'
            count = int(count_part.split()[1])  # number after repeat

            action = parts[1].strip()  # e.g. 'bolo "Coding mast hai"'
            if action.startswith("bolo"):
                message = action[5:].strip().strip('" ')
                for _ in range(count):
                    print(message)
            else:
                print("⚠️ Repeat command currently supports only 'bolo' action.")
        except:
            print("⚠️ Error in repeat syntax. Use: repeat 3 baar bolo \"message\"")

    elif code.strip().lower() == "rohan kaun hai":
        print("Rohan is founder of this language.")

    elif code.strip().lower() == "exit":
        print("\nThank you for using Rolang! Contact: ronk5811@gmail.com")
        exit()

    else:
        print("❓ Rolang samajh nahi payi: ", code)


def start_interpreter():
    print("Rolang Interpreter started. Type 'exit' to quit.")
    while True:
        code = input("📝 Rolang >>> ")
        if code.strip().lower() == "exit":
            print("\nThank you for using Rolang! Contact: ronk5811@gmail.com")
            break
        run_rolang(code)
