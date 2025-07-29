def gift():
    red = "\033[91m"
    reset = "\033[0m"
    heart = [
        "  ***     ***",
        " *****   *****",
        "******* *******",
        " *************",
        "  ***********",
        "   *********",
        "    *******",
        "     *****",
        "      ***",
        "       *"
    ]
    for line in heart:
        print(red + line + reset)
    print("\nfrom Koushik")

