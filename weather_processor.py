"""
Module providing weather data processing and flitering functionality.
"""
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt
import io
import base64

def process_three_days_data(data):
    """Filter and transform 3-day weather forecast data
    
    Args:
        data: Raw weather data
        
    Returns:
        list: Processed weather data
        
    Raises:
        Exception: If an error occurs during data processing
    """
    try:
        # Get WeatherElement section
        weather_elements = data["records"]["Locations"][0]["Location"][0]["WeatherElement"]
        # Processed result
        result = []
        
        # Iterate through each weather element
        for element in weather_elements:
            element_name = element["ElementName"]
            
            # Skip dewpoint temperature and non-numerical elements
            if element_name in ['露點溫度', '體感溫度', '舒適度指數', '風向', '天氣現象', '天氣預報綜合描述']:
                continue
                
            # Process time and values
            filtered_element = {
                "ElementName": element_name,
                "Time": []
            }
           
            for time_data in element["Time"]:
                # Process time format
                if "DataTime" in time_data:
                    # Remove seconds and timezone, keep date and hour only
                    time_str = time_data["DataTime"].split("+")[0]
                    # Keep only up to minutes
                    time_str = time_str[:16]
                elif "StartTime" in time_data:
                    # For fields using StartTime such as precipitation probability
                    time_str = time_data["StartTime"].split("+")[0]
                    time_str = time_str[:16]
                
                # Process values
                if "ElementValue" in time_data and len(time_data["ElementValue"]) > 0:
                    # Get corresponding value based on different weather element types
                    value = None
                    element_value = time_data["ElementValue"][0]
                    
                    if element_name == "溫度" and "Temperature" in element_value:
                        value = element_value["Temperature"]
                    elif element_name == "相對濕度" and "RelativeHumidity" in element_value:
                        value = element_value["RelativeHumidity"]
                    elif element_name == "風速" and "WindSpeed" in element_value:
                        value = element_value["WindSpeed"]
                    elif element_name == "3小時降雨機率" and "ProbabilityOfPrecipitation" in element_value:
                        value = element_value["ProbabilityOfPrecipitation"]
                    
                    # Add to result
                    if value is not None:
                        filtered_element["Time"].append([time_str, value])
            
            # Only add to result when there is time data
            if filtered_element["Time"]:
                result.append(filtered_element)
            
        return result
    
    except Exception as e:
        raise Exception(f"Error during data filtering: {str(e)}")


def process_one_week_data(data):
    """Filter and transform 1-week weather forecast data
    
    Args:
        data: Raw weather data
        
    Returns:
        list: Processed weather data
        
    Raises:
        Exception: If an error occurs during data processing
    """
    try:
        # Get WeatherElement section
        weather_elements = data["records"]["Locations"][0]["Location"][0]["WeatherElement"]
        
        # Processed result
        result = []
        
        # Iterate through each weather element
        for element in weather_elements:
            element_name = element["ElementName"]
            
            # Skip average dewpoint temperature and non-numerical elements
            if element_name in ['平均露點溫度', '最高體感溫度', '最低體感溫度', '最大舒適度指數', '最小舒適度指數', '風向', '天氣現象', '天氣預報綜合描述']:
                continue
                
            # Process time and values
            filtered_element = {
                "ElementName": element_name,
                "Time": []
            }
            
            for time_data in element["Time"]:
                # Process time format
                if "DataTime" in time_data:
                    # Remove seconds and timezone, keep date and hour only
                    time_str = time_data["DataTime"].split("+")[0]
                    # Keep only up to minutes
                    time_str = time_str[:16]
                elif "StartTime" in time_data:
                    # For fields using StartTime such as precipitation probability
                    time_str = time_data["StartTime"].split("+")[0]
                    time_str = time_str[:16]
                
                # Process values
                if "ElementValue" in time_data and len(time_data["ElementValue"]) > 0:
                    # Get corresponding value based on different weather element types
                    value = None
                    element_value = time_data["ElementValue"][0]
                    
                    if element_name == "平均溫度" and "Temperature" in element_value:
                        value = element_value["Temperature"]
                    elif element_name == "最高溫度" and "MaxTemperature" in element_value:
                        value = element_value["MaxTemperature"]
                    elif element_name == "最低溫度" and "MinTemperature" in element_value:
                        value = element_value["MinTemperature"]
                    elif element_name == "平均相對濕度" and "RelativeHumidity" in element_value:
                        value = element_value["RelativeHumidity"]
                    elif element_name == "風速" and "WindSpeed" in element_value:
                        value = element_value["WindSpeed"]
                    elif element_name == "12小時降雨機率" and "ProbabilityOfPrecipitation" in element_value:
                        value = element_value["ProbabilityOfPrecipitation"]
                    elif element_name == "紫外線指數" and "UVIndex" in element_value:
                        value = element_value["UVIndex"]
                    
                    # Add to result
                    if value is not None:
                        filtered_element["Time"].append([time_str, value])
            
            # Only add to result when there is time data
            if filtered_element["Time"]:
                result.append(filtered_element)
            
        return result
    
    except Exception as e:
        raise Exception(f"Error during data filtering: {str(e)}")


def process_thirtySix_hours_data(data):
    """Filter and transform 36-hour weather forecast data

    Args:
        data: Raw weather data

    Returns:
        list: Processed weather data

    Raises:
        Exception: If an error occurs during data processing
    """
    try:
        # Get WeatherElement section
        weather_elements = data["records"]["location"][0]["weatherElement"]
        # Processed result

        simplified_data = {
            'location': data['records']['location'][0]['locationName'],
        }

        for element in weather_elements:
            element_name = element['elementName']
            for time in element['time']:
                # 使用完整的開始時間作為鍵
                start_time = time['startTime']
                if start_time not in simplified_data:
                    simplified_data[start_time] = {}

                parameter = time['parameter']
                parameter_str = parameter['parameterName']
                if 'parameterUnit' in parameter:
                    parameter_str += f" {parameter['parameterUnit']}"

                # 尋找或創建對應時間的字典
                end_time = time['endTime']
                if end_time not in simplified_data[start_time]:
                    simplified_data[start_time][end_time] = {}

                simplified_data[start_time][end_time][element_name] = parameter_str
    
        # 獲取當前的日期和時間
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 遍歷所有的時間段
        for start_time in simplified_data:
            if start_time == 'location':
                continue
            for end_time in simplified_data[start_time]:
                # 如果當前時間在這個時間段內，則返回對應的天氣資訊
                if start_time <= now <= end_time:
                    result = simplified_data[start_time][end_time] # a python dictionary
                else:
                    # 如果沒有找到符合的時間段，則返回第一個天氣資訊
                    result = simplified_data[start_time][end_time]
       
        result_str = f'\nlocation: {simplified_data["location"]}\nweather summary: {result["Wx"]}\nprobability of precipitation: {result["PoP"]}\noutdoor thermal comfort index: {result["CI"]}\nmaximum temperature: {result["MaxT"]}\nminimum temperature: {result["MinT"]}\n'

        return result_str

    except Exception as e:
        raise Exception(f"Error during data filtering: {str(e)}")


def get_three_days_plot(data, ui_mode='terminal'):
    # translate elementName from Chinese to English
    elementName = ['Temperature', 'Relative humidity', 'Wind speed', 'Probability of precipitation']

    # first weather element
    Value = elementName[0]
    df = pd.DataFrame(data[0]['Time'], columns=['Time', Value])
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')
    df[Value] = pd.to_numeric(df[Value], errors='coerce')
    df_all = df.resample('3h').mean()

    # Merge the other weather elements
    for i in range(1,4):
        Value = elementName[i] 
        df = pd.DataFrame(data[i]['Time'], columns=['Time', Value])
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        df[Value] = pd.to_numeric(df[Value], errors='coerce')
        df_resampled = df.resample('3h').mean()
        df_all = pd.merge(df_all, df_resampled, on='Time', how='left')

    df_all = df_all.sort_index()
    df_future = df_all[df_all.index > pd.Timestamp.now()]

    if ui_mode == 'browser':
        fig, axes = plt.subplots(4, 1, figsize=(8, 6), sharex=True)

        for ax, col in zip(axes, df_all.columns):
            ax.scatter(df_all.index, df_all[col], color='gray', alpha=0.7)
            ax.scatter(df_future.index, df_future[col], color='red', alpha=0.7)
            ax.set_ylabel(col)
            ax.grid(True, which='major', axis='x')

        fig.suptitle('', fontsize=16, y=0.9)
        plt.gcf().autofmt_xdate()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        data_uri = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        return(data_uri)

    else:
        numerical_cols = df_all.columns
        df_all[numerical_cols] = df_all[numerical_cols].round().astype(int)

        new_df = df_all.resample('D').agg(['max', 'min'])

        units = ['C','%','','%']
        for col, unit in zip(df_all.columns, units):
            max_col = (col, 'max')
            min_col = (col, 'min')
            new_df[f"{col}_combined"] = new_df.apply(
                lambda row: f"[{row[max_col]}, {row[min_col]}] {unit}",
                axis=1
            )

        new_df = new_df.drop(columns=[(col, agg) for col in df_all.columns for agg in ['max', 'min']])

        new_df.index = new_df.index.strftime('%Y-%m-%d')

        table_str = tabulate(new_df, headers=df_all.columns, tablefmt='simple')

        return(table_str)


def get_one_week_ascii_table(data):
    # translate weather element names from Chinese to English
    elementName = ['T_avg', 'T_max', 'T_min', 'Rel humidity', 'Wind speed', 'Rain prob', 'UV index']

    # The first weather element
    Value = elementName[0]
    df = pd.DataFrame(data[0]['Time'], columns=['Time', Value])
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')
    df[Value] = pd.to_numeric(df[Value], errors='coerce')
    df_all = df.resample('D').mean()

    # Merge the other 6 weather elements
    for i in range(1,7):
        Value = elementName[i]
        df = pd.DataFrame(data[i]['Time'], columns=['Time', Value])
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        df[Value] = pd.to_numeric(df[Value], errors='coerce')
        df_resampled = df.resample('D').mean()
        df_all = pd.merge(df_all, df_resampled, on='Time', how='left')

    df_all = df_all.sort_index()
    df_all.index = df_all.index.strftime('%Y-%m-%d')

    table_str = tabulate(df_all, headers=df_all.columns, tablefmt='simple')

    return(table_str)
