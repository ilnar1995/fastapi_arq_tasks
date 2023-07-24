from typing import List
from fastapi import APIRouter, Depends

from arq_dashboard.queue import Queue, get_job_ids
from .schemas import TaskCreate, TaskView, TaskIdView
from arq.connections import ArqRedis
from src.redis import get_async_redis

task_router = APIRouter()


async def get_task_by_id(id, redis_pool) -> TaskView:
    """
    функыия для получения задачи по id
    """

    queue = Queue.from_name('arq:queue')
    job_info = await queue.get_job_by_id(id, redis_pool)

    status = job_info.status.value
    if job_info.result is not None:
        status = 'Ответ: ' + job_info.result
    if status == 'in_progress':
        status = 'в обработке'
    if status == 'queued':
        status = 'создана'
    execution_time = None
    if job_info.finish_time and job_info.start_time:
        execution_time = job_info.finish_time.timestamp() - job_info.start_time.timestamp()
    return TaskView(id=job_info.job_id, status=status, execution_time=execution_time)


@task_router.post('/task', response_model=TaskIdView)
async def create_task(item: TaskCreate, redis_pool: ArqRedis = Depends(get_async_redis)):
    """получение всех задач"""
    task = await redis_pool.enqueue_job("example_task", _queue_name=item.priority,
                                        sleep_time=item.slip_time)
    # job = Job(job_id=task.job_id, redis=redis_pool, _queue_name=item.priority)

    return TaskIdView(id=task.job_id)


@task_router.get('/task', response_model=List[TaskView])
async def get_tasks(redis_pool: ArqRedis = Depends(get_async_redis)):
    """создание задачи"""
    ids = await get_job_ids(redis_pool, 'name')
    jobs = [await get_task_by_id(id, redis_pool) for id in ids]

    return jobs


@task_router.get('/task/{id}', response_model=TaskView)
async def get_task(id: str, redis_pool: ArqRedis = Depends(get_async_redis)):
    """получение одной задачи"""
    return await get_task_by_id(id, redis_pool)
