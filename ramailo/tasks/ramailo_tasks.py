from celery import shared_task
from shared.helpers.logging_helper import logger


@shared_task(name="hello_world")
def hello_world():
    logger.info("ramailo_tasks hello_world: Executing")


@shared_task(name="execute_ramailo_task")
def execute_ramailo_task():
    logger.info("ramailo_tasks execute_ramailo_task: Executing")
    print("hwllo world")

