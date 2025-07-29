from .geoaiagent import serve

if __name__ == "__main__":
    print("This is the main program")
    import asyncio
    asyncio.run(serve())