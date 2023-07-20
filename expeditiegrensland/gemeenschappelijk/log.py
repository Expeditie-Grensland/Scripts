import traceback
import coloredlogs


def configureer_log(logger, debug):
    print()
    coloredlogs.install(
        logger=logger,
        fmt="%(asctime)s %(levelname)s %(message)s\n",
        level=("DEBUG" if debug else "INFO"),
    )


def log_error(logger, error: BaseException):
    logger.critical(error)
    logger.debug(
        "Tracering:\n"
        + "".join(traceback.format_list(traceback.extract_tb(error.__traceback__)))
    )
