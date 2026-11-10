from workers.celery_app import celery_app


@celery_app.task
def add_twoNum(a: int, b: int) -> int:
    result = a + b
    print(f"Processing task: {a} + {b}")
    print(f"${a} + {b} = {result}")
    return result
