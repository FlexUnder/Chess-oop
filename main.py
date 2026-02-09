import menu


def main():
    logo = ''.join(open('assets/logo.txt').readlines())
    menu.start(logo)


if __name__ == "__main__":
    main()