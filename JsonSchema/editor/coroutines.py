import asyncio

async def fetch_data(delay):
    print("Feteching Data...")
    await asyncio.sleep(delay) # simulates an i/o operation that simulates a task
    print("data fetched")
    return {"Data" : "some Data"}

# coroutine object
async def main():
    print("start of the main coroutine")
    task = fetch_data(2)
    # await the fetch data  pausing execution, until it completes
    result = await task
    print(f"Recieved Data : {result}")
    print("End of main coroutine")

# start the event loop and runs the 'main" coroutine.
asyncio.run(main())
# print(main()) returns a coroutine object