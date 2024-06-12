import asyncio

shared_resource = 0

lock = asyncio.Lock()

async def modify_shared_resource():
    global shared_resource
    async with lock:
        # critical section starts
        print(f"shared modification before: {shared_resource}")
        shared_resource += 1
        await asyncio.sleep(1)
        print(f"shared modification after: {shared_resource}")
        # end critcal section


async def main():
    # all 5 of the coroutines are being created and run at the same time
    await asyncio.gather(*(modify_shared_resource() for _ in range(5)))

asyncio.run(main())