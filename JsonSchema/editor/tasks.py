import asyncio

async def fetch_data(id, delay):
    print(f"coroutine {id} starting to fetch data....")
    await asyncio.sleep(delay) # simulates an i/o operation that simulates a task
    print("data fetched")
    return {"Data" : f"sample from coroutine {id}", "id" : id}

# coroutine object
async def main():
    # print("start of the main coroutine")
    # task1 = asyncio.create_task(fetch_data(1, 2))
    # task2 = asyncio.create_task(fetch_data(2, 3))
    


    # res1 = await task1
    # res2 = await task2

    # task3 = asyncio.create_task(fetch_data(3, 1))


    # res3 = await task3

    # print(res1, res2, res3)

    results = await asyncio.gather(fetch_data(1,2), fetch_data(2, 3), fetch_data(3, 1))
    for result in results:
        print(result)

# start the event loop and runs the 'main" coroutine.
asyncio.run(main())
# print(main()) returns a coroutine object