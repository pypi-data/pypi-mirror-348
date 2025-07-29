import asyncio
from typing import Dict
from Osdental.ServicesBus.ServicesBus import ServicesBus
from Osdental.Utils.Logger import logger
from Osdental.Handlers.Instances import conn_str, queue_name

class TaskQueue:
    """Queue to manage tasks in order and asynchronously."""

    def __init__(self):
        self.service_bus = ServicesBus(conn_str, queue_name)
        self.queue = asyncio.Queue()
        

    def start_processing(self):
        """Start processing tasks in the background."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(self.process_tasks())


    async def enqueue(self, message:Dict[str,str]):
        """Add a task to the queue."""
        await self.queue.put(message)


    async def process_tasks(self):
        """Process tasks from the queue in order."""
        while True:
            message = await self.queue.get()
            try:
                await self.service_bus.send_message(message)
            except Exception as e:
                logger.error(f'Message queuing error: {str(e)}')
            finally:
                self.queue.task_done()


task_queue = TaskQueue()
task_queue.start_processing()