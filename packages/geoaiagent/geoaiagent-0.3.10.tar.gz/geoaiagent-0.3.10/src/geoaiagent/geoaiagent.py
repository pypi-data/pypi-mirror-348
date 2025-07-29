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

@server.tool()
async def get_soil_info(
    oid: int = Tool(name="oid", description="要查询的OID编号",inputSchema={
            "type": "integer"
        }),
    resource_uri: str = Tool(name="resource_uri",
        description="资源标识符",inputSchema={
            "type": "integer"
        }
    )
) -> str:
    """根据OID查询土壤信息"""
    try:
        # 获取CSV数据
        csv_data = await read_excel_resource(resource_uri)
        
        # 转换为DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        # 执行查询
        result = df[df['OID'] == oid]
        
        if not result.empty:
            soil_info = result.iloc[0].to_dict()
            return f"OID {oid} 的土壤类型为 {soil_info['SOIL_ID']}"
        else:
            return f"未找到OID {oid} 对应的记录"
            
    except ValueError as e:
        return f"错误: {str(e)}"
    except Exception as e:
        return f"内部错误: {str(e)}"
# @server.list_tools()
# async def list_tools() -> list:
#     """
#     Lists all available tools.
#     """
#     return ["add_geo", "sub_geo"]

@server.resource("/soil-data/{uri}")
async def read_excel_resource(uri:str) -> str:
    """读取本地Excel文件资源"""
    
    parsed = urlparse(uri)
    if parsed.scheme != "file":
        raise ValueError("只支持 file:// 协议")
    
    # 转换路径格式（Windows需要特殊处理）
    file_path = Path(parsed.path.lstrip('/')).resolve()
        
    # 读取Excel文件
    df = pd.read_excel(file_path, engine='openpyxl')
    return df.to_csv(index=False)
    


def doit():
    print("Hello from aiagent!")
    server.run()
    
if __name__ == "__main__":
    doit()
    