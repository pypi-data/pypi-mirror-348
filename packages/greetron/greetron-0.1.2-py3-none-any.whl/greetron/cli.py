import argparse
from greetron.greetings import get_random_greeting, get_random_goodbye

def main():
    parser = argparse.ArgumentParser(description="Generate greetings or goodbyes.")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.2')
    parser.add_argument('--owner', action='store_true', help="Show the creator of this tool")    
    parser.add_argument("type", nargs='?', choices=["greeting", "goodbye"], help="Type of message to generate")
    parser.add_argument("--name", type=str, default=None, help="Optional name to personalize the message")
    parser.add_argument("--mode", choices=["formal", "informal"], default="formal", help="Tone of the message")

    args = parser.parse_args()

    if args.owner:
        print("Created by Aryan Bhan")
        return
    # If 'type' argument is missing, enter interactive mode
    if not args.type:
        # Interactive prompt
        while True:
            msg_type = input("Would you like a greeting(g) or goodbye(b)? (g/b): ").strip().lower()
            if msg_type in ["greeting", "g"]:
                args.type = "greeting"
                break
            elif msg_type in ["goodbye", "bye", "b"]:
                args.type = "goodbye"
                break
            else:
                print("Please enter 'greeting' or 'goodbye'.")

        mode = input("Choose mode (formal/informal) [informal]: ").strip().lower()
        if mode in ["formal", "informal"]:
            args.mode = mode
        else:
            args.mode = "informal"

        name = input("Enter a name (or press Enter to skip): ").strip()
        args.name = name if name else None

    # Generate and print the message
    if args.type == "greeting":
        print(get_random_greeting(name=args.name, mode=args.mode))
    elif args.type == "goodbye":
        print(get_random_goodbye(name=args.name, mode=args.mode))
    else:
        parser.print_help()