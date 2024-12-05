import asyncio
from datetime import datetime
import redis
from celery import Celery
from core.config import settings
from common.response.response_one_c import OneCParser
from common.response.response_b24 import Bitrix24
from core.path_conf import STORE_DIR

# TO DO Bitrix update
app = Celery(
    "task",
    broker=settings.redis_url(3),
    backend=settings.redis_url(4),
    broker_connection_retry_on_startup=True,
)

r = redis.Redis.from_url(settings.redis_url(4))

# Create an event loop if needed
loop = asyncio.get_event_loop()


# Need check date
async def product_updater():
    date = datetime.now().strftime("%Y-%m-%d")
    await OneCParser().create_products(f"{STORE_DIR}/{date}.xml")


@app.task(bind=True)
def my_task(self):
    print(self)
    if r.get("my_task_lock"):
        print("Task is already running.")
        return

    r.set("my_task_lock", "1", ex=60)  # Lock for 60 seconds

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Run coroutine in existing loop
            loop.create_task(product_updater())
        else:
            loop.run_until_complete(product_updater())
    finally:
        r.delete("my_task_lock")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, my_task.s(), name="run my_task every minute")


if __name__ == "__main__":
    app.start()
