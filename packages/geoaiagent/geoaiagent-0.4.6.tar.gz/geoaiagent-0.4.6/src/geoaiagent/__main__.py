from .geoaiagent import to_run

async def main():
    await to_run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())