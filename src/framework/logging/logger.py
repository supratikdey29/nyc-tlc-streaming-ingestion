import logging
#import uuid


class FrameworkLogger:
    """
    Centralized logger for the ingestion framework.

    Creates one logger per framework component while sharing
    the same pipeline Run ID across the entire execution.
    """

    #_run_id = str(uuid.uuid4())[:8]
    _run_id = None

    @classmethod
    def set_run_id(cls, run_id: str):
        cls._run_id = run_id

    @classmethod    
    def get_logger(cls, component: str):

        logger = logging.getLogger(component)

        logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | Run=%(run_id)s | %(component)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            handler.setFormatter(formatter)

            logger.addHandler(handler)

        # Remove any old filters so the component name
        # doesn't get duplicated when get_logger() is called again.
        logger.filters.clear()

        class ContextFilter(logging.Filter):

            def filter(self, record):

                #record.run_id = FrameworkLogger._run_id
                record.run_id = FrameworkLogger._run_id or "NO-RUN"
                record.component = component

                return True

        logger.addFilter(ContextFilter())

        logger.propagate = False

        return logger