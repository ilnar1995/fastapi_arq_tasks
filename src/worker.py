import sys

from src.task.tasks import example_task, clean_task_instances

sys.path.extend(["./"])

from arq.connections import RedisSettings
from src.config import REDIS_HOST


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


FUNCTIONS: list = [
    example_task,
]


class WorkerSettings:
    max_jobs = 5
    queue_name = 'high'
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(host=REDIS_HOST)
    functions: list = FUNCTIONS
    keep_result_forever = True
    cron_jobs = [clean_task_instances]
