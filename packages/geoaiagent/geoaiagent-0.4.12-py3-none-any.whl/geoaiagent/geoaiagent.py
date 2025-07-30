from mcp.server import FastMCP
import pandas as pd
from pathlib import Path
from mcp import Tool
from urllib.parse import urlparse

from sklearn.model_selection import train_test_split
import xgboost as xg
from io import StringIO


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
    
@server.tool()
async def presict_capacity(
    train_uri: str = Tool(name="train_uri", description="训练集路径，请使用uri形式输入，且仅支持file://协议，如file:///D:/train.csv",inputSchema={"type": "string"}),
    test_data: str = Tool(name = "test_data",description="自变量，请输入土壤类型，N、P、K含量，温度，湿度，ph，降雨量，并且以逗号隔开，总共两行，第一行为列标签,值为[N,P,K,温度,湿度,ph,降雨]如果不匹配则会出现错误，第二行为具体数值。如果没有明确指出，请先调用其它工具进行查阅，并且在此参数处输入“help”以退出该函数",inputSchema={"type": "string"})
) -> str:
    """
    根据用户所给的土壤类型，N、P、K含量，温度，湿度，ph，降雨量，得到最佳的推荐作物
    """
    
    if test_data == "help":
        return ""
    try:
        df = await read_excel_resource(train_uri)
        # 使用StringIO模拟文件对象
        data_io = StringIO(df)
        xgtest_io = StringIO(test_data)
        
        xgtest = pd.read_csv(xgtest_io)
        data = pd.read_csv(data_io)
        x_train,x_text,y_train,y_text = train_test_split(data.iloc[:,1:50]#取data第二到五十一列的所有数据
                                                        ,data.iloc[:,0]#取data第一列的所有数据
                                                        ,test_size = 0.3)#设置分割的比例为7：3
                                                        #随机划分可以设置种子
        print(x_train)
        print(y_train)
        xgtrain = xg.DMatrix(x_train,label = y_train)
            #训练集
                #用于迭代
        xgtest = xg.DMatrix(xgtest,label = y_text)



        #设置参数
        param = {'booster':'gbtree',#指定弱学习器类型（gbtreg,blinear）,默认值为gbtree,一般都使用默认值
                'learning_rate':'0.3',#学习率(0~1，0.3),指模型迭代过程中对新学习器的信任度，学习率过大可能会造成模型震荡，学习率过小可能造成过拟合，并且造成性能浪费
                                    #学习率0.1和0.05在1000r的时候有低学习率效果好30%左右，在100r的时候则高学习率则更好
                'gamma':'0.01',#伽马值(0~1，0)，指定模型树在分支时剪枝所需的最小损失值，值越大越容易剪枝，效果类似于学习率越低
                'max_depth':'8',#最大树深度，即判断决策树的深度，当树深度较高的时候，模型会学习到非常多的特征，模型会很复杂，但同时，模型的拟合度也会更高，过拟合的可能性也更高
                                #当树深度较低时，树的复杂度会很低，不容易出现过拟合，但是预测的精度也会非常低
                                #一般的推荐值在3~10之间
                #'max_leaf_nodes':'2',#最大分支数，与max_depth类似，不同的是，它增加的是横向的复杂度，默认为2，设置为其它值会将max_depth重置回默认值
                'subsample':'0.5',#随机采样比例(0~1,1)，控制每棵树在数据集中采样的比例，调低这个数值可以避免过拟合
                                #感觉影响不太大
                'colsample_bytree':'0.7',#特征采样比例(0~1,1)，与subsample类似，感觉影响也不太大
                'alpha':'1',#正则化参数L1(0~，1)，惩罚值，让出现频率过高的特征对模型的影响程度趋于正常，对于某些极端的数据，需要适当增大正则化值以避免过拟合
                'lambda':'1',#正则化参数L2(0~, 1)，效果类似于alpha
                }

            #迭代轮数
        train_round = 25
            #说明监督列表
        watchlist = [(xgtrain,'lable')]

        #训练模型
        modle = xg.train(param,xgtrain,train_round,watchlist)

        pre_get = modle.predict(xgtest)

        print(pre_get)
        crop_type = {1:"小麦",2:"玉米"}
    
        return crop_type[int(pre_get[0] + (0.5 if pre_get[0] > 0 else -0.5))]
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