import pandas as pd

def get_soil_id_from_excel(excel_path, input_fid):
    """
    根据id获取土壤类型
    输入数据表路径，待检索土地的oid
    输出土壤soil_id
    """
    try:
        # 读取 Excel 文件（默认读取第一个工作表）
        df = pd.read_excel(excel_path)
        
        # 检查必要列是否存在
        if 'OID' not in df.columns or 'SOIL_ID' not in df.columns:
            print("错误：Excel 中缺少 FID 或 SOIL_ID 列")
            return None
            
        # 查找匹配的 FID
        result = df.loc[df['OID'] == input_fid, 'SOIL_ID']
        
        if not result.empty:
            return result.values[0]  # 返回第一个匹配项的 SOIL_ID
        else:
            return None
            
    except FileNotFoundError:
        print(f"错误：文件 {excel_path} 不存在")
        return None
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return None
    
print(get_soil_id_from_excel(r"D:\_Endless\AI智能体\testdata\testmap\testtable_TableToExcel.xlsx",6))