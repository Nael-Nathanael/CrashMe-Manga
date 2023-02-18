class PrettyColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_primary(tag, text):
    print(f"{PrettyColors.OKBLUE}{tag}{PrettyColors.ENDC}: {text}")


def print_warning(tag, text):
    print(f"{PrettyColors.WARNING}{tag}{PrettyColors.ENDC}: {text}")


def print_success(tag, text):
    print(f"{PrettyColors.OKGREEN}{tag}{PrettyColors.ENDC}: {text}")


def print_danger(tag, text):
    print(f"{PrettyColors.FAIL}{tag}{PrettyColors.ENDC}: {text}")
