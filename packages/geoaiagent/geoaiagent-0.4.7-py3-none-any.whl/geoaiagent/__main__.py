from .geoaiagent import to_run

def main():
    to_run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())