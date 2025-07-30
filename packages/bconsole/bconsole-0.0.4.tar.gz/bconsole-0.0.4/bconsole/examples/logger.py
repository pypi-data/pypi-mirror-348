from bconsole import ColoredLogger

logger = ColoredLogger()

logger.verbose("This is a verbose message.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.log("This is also an info message.", level="info")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
