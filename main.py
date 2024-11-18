from icecream import ic, install
from app import *


def main():
    ic("Comet-tracker has been started.")
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    install()
    Logger.clear()
    main()
