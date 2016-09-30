from colorama import init, Fore, Back, Style
import colorlog
import argparse


def showcase_color_ama():
    init(autoreset=True)

    messages = [
        'blah blah blah blah',
        (Fore.LIGHTYELLOW_EX + Style.BRIGHT + Back.MAGENTA + 'Alert!!!'),
        'blah blah blah'
    ]

    for m in messages:
        print(m)


def showcase_color_log():
    logger = colorlog.getLogger()
    logger.setLevel(colorlog.colorlog.logging.DEBUG)

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter())
    logger.addHandler((handler))

    logger.debug("Debug Message")
    logger.info("Information message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


def showcase_arg_prase(a, b):
    return a + b


if __name__ == '__main__':
    #showcase_color_log()
    """
    parser = argparse.ArgumentParser(
        description="Add two numbers"
    )
    parser.add_argument('-a',
                        help='First value',
                        type=float,
                        default=0)
    parser.add_argument('-b',
                        help='Second value',
                        type=float,
                        default=0)
    args = parser.parse_args()
    print(showcase_arg_prase(args.a, args.b))
    """