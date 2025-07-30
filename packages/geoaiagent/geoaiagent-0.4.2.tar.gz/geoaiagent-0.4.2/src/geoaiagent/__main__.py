from .geoaiagent import to_run

async def thisismain():
    await to_run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(thisismain())
