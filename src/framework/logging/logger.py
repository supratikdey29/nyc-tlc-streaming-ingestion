import logging
import uuid


class FrameworkLogger:
    """
    Centralized logger for the ingestion framework.
    """

    _logger = None
    _run_id = str(uuid.uuid4())[:8]

    @classmethod
    def get_logger(cls, component: str):

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger("nyc_tlc_framework")

        logger.setLevel(logging.INFO)

        if not logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | Run=%(run_id)s | %(component)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            handler.setFormatter(formatter)

            logger.addHandler(handler)

        class ContextFilter(logging.Filter):

            def filter(self, record):

                record.run_id = FrameworkLogger._run_id
                record.component = component

                return True

        logger.addFilter(ContextFilter())

        cls._logger = logger

        return logger