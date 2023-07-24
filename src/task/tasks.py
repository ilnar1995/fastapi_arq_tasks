import asyncio
import datetime
from arq.connections import RedisSettings, create_pool
from arq.cron import CronJob
from arq_dashboard.queue import get_result_job_ids, Queue
from src.config import REDIS_HOST, KEEP_RESULT


async def get_task_by_id(id, redis_pool):
    """
    проверка по прошедшего времени с момента завершения задачи
    """
    queue = Queue.from_name('arq:queue')
    job_info = await queue.get_job_by_id(id, redis_pool)
    execution_time = 0
    if job_info.finish_time and job_info.start_time:
        execution_time = datetime.datetime.now().timestamp() - job_info.finish_time.timestamp()

    return execution_time > KEEP_RESULT


async def example_task(ctx, sleep_time: int):
    """
    пример задачи для выполения в воркере
    """
    await asyncio.sleep(sleep_time)
    return 'Это ответ задачи.'


async def clean_task_func(ctx):
    """
    удаляем старые завершенные задачи
    """
    redis = await create_pool(RedisSettings(REDIS_HOST), default_queue_name='high')

    # получаем множество id завершенных задач
    ids = await get_result_job_ids(redis)

    # сортируем множество на старые задачи и прибавляем приставку для получения списка ключей redis
    jobs = ["arq:result:" + x.decode('utf-8') for x in ids if await get_task_by_id(x.decode('utf-8'), redis)]

    # удаляем старые задачи
    if len(jobs) > 0:
        async with redis.pipeline(transaction=True) as tr:
            tr.delete(*jobs)
            await tr.execute()


# экземпляр класса CronJob для настрек запуска периодической задачи
clean_task_instances = CronJob(
    name='clean_task_func',
    month=None,
    day=None,
    weekday=None,
    hour=None,
    minute=None,
    second=10,
    microsecond=1_456,
    run_at_startup=False,
    unique=False,
    job_id="1",
    timeout_s=1,
    keep_result_s=1,
    keep_result_forever=False,
    max_tries=30,
    coroutine=clean_task_func)
