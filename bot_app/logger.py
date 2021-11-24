import logging

# Logging setup
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(module)s(%(lineno)d) | %(funcName)s() || %(message)s ||",
                     level=logging.INFO)

logger = logging.getLogger(__name__)
