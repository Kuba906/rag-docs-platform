import structlog

def setup_logging():
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(20))
