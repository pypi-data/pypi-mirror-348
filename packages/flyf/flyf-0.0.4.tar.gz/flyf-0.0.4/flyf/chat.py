import argparse

def iChat(message):
    print(f'Ai:{message}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", type=str, help="Input the message content")
    parser.add_argument("-f", "--flyf", action="store_true", help="Display information")
    args = parser.parse_args()

    if args.flyf:
        print("Star us on GitHub if you like it! 🌟 —— https://github.com/AiFLYF/FLYF")
    elif args.message:
        iChat(args.message)
    else:
        iChat("Flyf is still under development. Please stay tuned 🙌")

if __name__ == "__main__":
    main()