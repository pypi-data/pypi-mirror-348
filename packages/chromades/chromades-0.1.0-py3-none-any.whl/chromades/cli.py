import argparse
import time
from chromades.progress import cool_progress_bar
from chromades.colors import warning, success, info

def main():
    parser = argparse.ArgumentParser(description="Chromades CLI — terminal graphics toolkit")
    parser.add_argument(
        "--progress", 
        type=int, 
        metavar="N", 
        help="Show a cool progress bar counting to N"
    )
    parser.add_argument(
        "--message", 
        choices=["warning", "success", "info"], 
        help="Show a colored message"
    )
    args = parser.parse_args()

    if args.progress:
        for i in cool_progress_bar(range(args.progress)):
            time.sleep(0.05)  # Simuluj práci
        print(success("Progress finished!"))

    if args.message:
        if args.message == "warning":
            print(warning("This is a warning message!"))
        elif args.message == "success":
            print(success("This is a success message!"))
        elif args.message == "info":
            print(info("This is an info message!"))

if __name__ == "__main__":
    main()
