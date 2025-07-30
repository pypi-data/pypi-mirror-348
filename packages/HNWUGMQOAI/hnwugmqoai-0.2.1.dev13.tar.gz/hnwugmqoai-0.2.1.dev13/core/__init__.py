import loguru
from tqdm import tqdm

loguru.logger.remove()
loguru.logger.add("app.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
loguru.logger.add(lambda msg: tqdm.write(msg, end=""))