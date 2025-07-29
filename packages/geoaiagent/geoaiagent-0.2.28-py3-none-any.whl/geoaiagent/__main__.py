from geoaiagent import serve

def thisismain():
    import asyncio
    
    asyncio.run(serve())

if __name__ == "__main__":
    print("This is the main program")
    thisismain()