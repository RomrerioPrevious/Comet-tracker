from icecream import ic, install
from app import *


def main():
    ...


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    install()
    Logger.clear()
    main()
