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

@server.tool()
async def read_grain_data(year: int = Tool(name="year", description="要查询的年份，仅包含2021,2022,2023年",inputSchema={"type": "integer"}),
                          name:str = Tool(name="name", description="要查询城市的名称，可选有[仁和区,米易县,盐边县,西昌市,会理市,盐源县,会东县,宁南县,喜德县,冕宁县]，如果待查询的城市不包含其中，请进行网络搜索",inputSchema={"type": "string"}),
                          resource_uri: str = Tool(name="resource_uri",description="资源标识符，文件名形为‘安宁河流域粮食数据20xx’，其中xx表示具体的年份，输入时请用具体的年份代替输入，文件路径不变",inputSchema={"type": "integer"
        }
    )) -> dict:
    """
    查询某地区某年份的耕地数据，当用户需要你对某地区的耕地情况进行分析的时候，请使用此工具。
    参数描述如下：
    year：类型为int，表示要查询的年份，仅包含2021,2022,2023年
    name：类型为str，表示要查询城市的名称，可选有[仁和区,米易县,盐边县,西昌市,会理市,盐源县,会东县,宁南县,喜德县,冕宁县]，如果待查询的城市不包含其中，请进行网络搜索
    resource_uri：类型为str，表示资源标识符，请使用uri形式输入，且仅支持file://协议，文件名形为‘安宁河流域粮食数据20xx’，其中xx表示具体的年份，输入时请用具体的年份代替输入，如果用户没有输入文件路径，请依此输入file:///soildata/安宁河流域粮食数据20xx.xlsx
    """
    try:
        # 获取CSV数据
        csv_data = await read_excel_resource(resource_uri)
        
        # 转换为DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        if year not in [2021, 2022, 2023]:
            return f"错误：{year} 年份没有耕地数据，请检查输入后重新尝试"
        
        if name not in ['仁和区', '米易县', '盐边县', '西昌市', '会理市', '盐源县', '会东县', '宁南县', '喜德县', '冕宁县']:
            return f"错误：{name} 没有该城市的数据，请等待数据更新，或者检查输入后重新尝试"
        
        if df.empty:
            return f"未找到{name}在{year}年份的耕地数据"
        
        # 执行查询
        result = df[df['名字'] == name]
        
        if not result.empty:
            soil_info = result.to_dict()
            return soil_info
        else:
            return f"未找到对应的数据，请重新检查输入格式、城市名称或年份是否正确"
            
    except ValueError as e:
        return f"错误: {str(e)}"
    except Exception as e:
        return f"内部错误: {str(e)}"

def to_run():
    print("GeoAIAgent 启动成功！")
    server.run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(to_run())