# Configure the logger
import logging
import os
from datetime import datetime

logger = None


def setup_logger(log_dir, name_prefix):
	# Prevent re-running basicConfig and adding duplicate handlers
	global logger
	if logger is not None:
		return logger  # Already configured

	os.makedirs(log_dir, exist_ok=True)

	log_file = f"{log_dir}/{name_prefix}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

	logging.basicConfig(
		format="[%(asctime)s] %(module)s - %(funcName)s - %(levelname)s - %(message)s",
		datefmt="%H:%M:%S",
		handlers=[
			logging.StreamHandler(),
			logging.FileHandler(log_file),
		],
	)

	# Suppress third-party logs by setting root logger to ERROR
	logging.getLogger().setLevel(logging.ERROR)
	# Suppress specific noisy third-party loggers
	logging.getLogger("fontTools.ttLib").setLevel(logging.ERROR)
	logging.getLogger("fontTools.subset").setLevel(logging.ERROR)

	# Create a logger and set independent log level
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	return logger


def get_logger():
	if logger is None:
		raise RuntimeError("Logger has not been initialized. Call setup_logger(path) first.")
	return logger
