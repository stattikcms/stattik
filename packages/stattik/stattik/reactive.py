from collections import UserDict
from aioreactive import AsyncSubject, AsyncAnonymousObserver

class Blackboard(UserDict):

    def __init__(self) -> None:
        super().__init__()
        self.add_topic('index')

    def add_topic(self, topic):
        self[topic] = AsyncSubject()

    async def subscribe(self, topic, awaitable):
        if not topic in self:
            self.add_topic(topic)
        subscription = await self[topic].subscribe_async(AsyncAnonymousObserver(awaitable))
        return subscription

    async def publish(self, topic, val):
        await self[topic].asend(val)
