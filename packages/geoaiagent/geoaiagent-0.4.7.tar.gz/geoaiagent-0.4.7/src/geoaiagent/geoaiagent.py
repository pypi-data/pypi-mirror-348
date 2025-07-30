from mcp.server import FastMCP
import pandas as pd
from pathlib import Path
from mcp import Tool
from urllib.parse import urlparse


server = FastMCP("geoaiagent")
    
@server.tool()
async def add_geo(lat: float, lon: float) -> float:
    """
    Adds a new geolocation to the database.
    """
    return lat + lon
@server.tool()
async def sub_geo(lat: float, lon: float) -> float:
    """
    Subtracts a geolocation from the database.
    """
    return lat - lon

# @server.resource("/soil-data/{uri}")
# async def read_excel_resource(uri:str) -> str:
#     """读取本地Excel文件资源"""
    
#     parsed = urlparse(uri)
#     if parsed.scheme != "file":
#         raise ValueError("只支持 file:// 协议")
    
#     # 转换路径格式（Windows需要特殊处理）
#     file_path = Path(parsed.path.lstrip('/')).resolve()
        
#     # 读取Excel文件
#     df = pd.read_excel(file_path, engine='openpyxl')
#     return df.to_csv(index=False)

async def to_run():
    print("GeoAIAgent 启动成功！")
    await server.run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(to_run())