import coloredlogs


def configureer_log(debug=False):
    print()
    coloredlogs.install(
        fmt="%(asctime)s %(levelname)s %(message)s\n",
        level=("DEBUG" if debug else "INFO"),
    )
