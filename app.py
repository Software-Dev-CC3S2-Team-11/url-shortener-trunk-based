import json


def main():
    with open("config.json") as f:
        config = json.load(f)
        print(config)


if __name__ == "__main__":
    print('Versión 0')
    main()
