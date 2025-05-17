import textnode

def main():
    node = textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://boot.dev")
    print(node)

if __name__ == "__main__":
    main()
