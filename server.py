import os
import argparse

from mcp.server.fastmcp import FastMCP

from weather_fetcher import (
    fetch_three_days_forecast,
    fetch_one_week_forecast,
    fetch_thirtySix_hours_forecast,
    get_valid_location,
    validate_api_key,
    VALID_LOCATIONS
)
from weather_processor import (
    process_three_days_data, 
    process_one_week_data, 
    process_thirtySix_hours_data, 
    get_three_days_plot, 
    get_one_week_ascii_table
)
from image2ascii import image_to_colored_ascii, image_to_base64

# Get API Key
CWA_API_KEY = os.getenv("CWA_API_KEY")

parser = argparse.ArgumentParser(description='runtime environment for the tool')
parser.add_argument("-m","--ui_mode",
                    help="Runtime environment of the LLM: 'browser' or 'terminal'", type=str, default='terminal')
parser.add_argument("-w","--ascii_width",
                    help="Width of the output text block: between 80 and 120 characters", type=int, default=120)

args = parser.parse_args()

# Initialize MCP Server
mcp = FastMCP("Taiwan Weather API")

@mcp.tool()
def get_weather_forecast(location_name: str, num_days: str) -> str:
    """Get 3-day or 1-week weather forecast for the specified city/county in Taiwan
    
    Args:
        num_days (str): three or seven

        location_name (str): city/county, must be a valid Taiwan city/county name
        Valid city/county names are: 
            宜蘭, 花蓮, 臺東, 澎湖, 金門, 連江, 
            臺北, 新北, 桃園, 臺中, 臺南, 高雄, 
            基隆, 新竹縣, 新竹市, 苗栗, 彰化, 南投, 
            雲林, 嘉義縣, 嘉義市, 屏東

        So, when using this tool, convert location name into one of the above in tranditional Chinese: for example input "臺北" instead of "Taipei", "花蓮" instead of "Hualien", etc.
        
    Returns:
        One of the following tables:

        - A 3-day weather forecast table listing the predicted ranges of temperature, relative humidity, wind speed (Beaufort scale), and probability of precipitation of the specified city in Taiwan over the current and next 3 days.
        - A 7-day weather forecast table listing the predicted temperature (avg, max, and min), relative humidity, wind speed (Beaufort scale), probability of precipitation, and UV index of the specified city in Taiwan over a 7-day period.
    """
    # Validate location name
    location = get_valid_location(location_name)

    if num_days == 'three':
        # Get weather data
        raw_data = fetch_three_days_forecast(location, CWA_API_KEY)
    
        # Filter the data
        processed_data = process_three_days_data(raw_data)

        # Generate ascii plot
        ascii_table = get_three_days_plot(processed_data)
    
    else:
        raw_data = fetch_one_week_forecast(location, CWA_API_KEY)

        # Filter the data
        processed_data = process_one_week_data(raw_data)

        # Generate ascii table
        ascii_table = get_one_week_ascii_table(processed_data)

    ascii_table = location + '\n' + ascii_table

    if args.ui_mode == "browser":
            return(f"""<pre style="font-family: monospace; white-space: pre;">{ascii_table}</pre>""")

    return f"```text\n\n{ascii_table}\n```"

           
@mcp.tool()
def get_current_weather_conditions(location_name: str) -> str:
    """Get the current weather of the specified city/county in Taiwan. 

    Args:
        location_name (str): city/county, must be a valid Taiwan city/county name

        Valid city/county names include: 
            宜蘭, 花蓮, 臺東, 澎湖, 金門, 連江,
            臺北, 新北, 桃園, 臺中, 臺南, 高雄,
            基隆, 新竹縣, 新竹市, 苗栗, 彰化, 南投,
            雲林, 嘉義縣, 嘉義市, 屏東

        So, when using this tool, convert location name into one of the above in tranditional Chinese: for example input "臺北" instead of "Taipei", "花蓮" instead of "Hualien", etc.

    Returns:
        A summary of the current weather conditions, including probability of precipitation, outdoor thermal comfort index, and max and min of temperature, of the specified city in Taiwan.
    """
    # Validate location name
    location = get_valid_location(location_name)
 
    # Get weather data
    raw_data = fetch_thirtySix_hours_forecast(location, CWA_API_KEY)

    # Locate and transform the data
    weather_summary = process_thirtySix_hours_data(raw_data)

    return f"```\n{weather_summary}\n```"


@mcp.tool()
def get_current_weather_image(region: str, wavelength: str) -> str:
    """
    Get the satellite weather image of Taiwan or East Asia. The imagery updates very 10 minutes.
 
    Args:
        region (str): either Taiwan or East Asia 
        wavelength (str): infrared, visible, or radar
       
        - The covered region in the Taiwan image includes only Taiwan
        - The covered regions of East Asia in the image include Beijing, Chongqing, Hanoi, Ho Chi Minh, Singapore, Brunei, Shenzhen, Hong Kong, Manila, Shanghai, Taipei, Seoul, Osaka, Tokyo, and Sapporo.

        - Infrared weather image is best for thunderstorm monitoring, and nighttime cloud tracking.
        - Visible-light weather image is best for fog, haze, daytime clouds, and cloud edges detection.
        - Radar reflectivity weather image is best for live precipitation, storm tracking, and warnings.

    Returns:
        Weather image in a preformatted style based on the runtime environment.

        - If the tool is running in 'terminal' mode, the image is converted to colored ASCII characters and wrapped in a Markdown code block (using triple backticks) to preserve alignment and monospaced formatting.
        - If running in 'browser' mode, the output is wrapped in HTML-safe base64-encoded <img> tags for direct rendering in web-based interfaces.
        The LLM does not need to infer the runtime environment. Instead, it should display the output according to the provided format. The tool ensures the output is pre-formatted for the intended environment.
    """
    isRadar = False

    # Determine the url based on the input parameters

    if wavelength == 'infrared':
        url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-C0042-002.jpg"
        if region == 'East Asia':
            url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-B0032-002.jpg"

    elif wavelength == 'visible':
        url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-C0042-008.jpg"
        if region == 'East Asia':
            url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-B0032-001.jpg"

    elif wavelength == 'radar':
        isRadar = True
        url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-A0058-003.png"
        if region == 'East Asia':
            url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-A0058-001.png"

    else:
        url = "https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-C0042-002.jpg" # default is infrared image of Taiwan

    if args.ui_mode == 'browser':
        img_base64 = image_to_base64(url)
        return f'<div><img src="data:image/png;base64,{img_base64}" /></div>'

    ascii_block = image_to_colored_ascii(url, args.ascii_width, isRadar)

    return("```text\n" + ascii_block + "\n```")


if __name__ == "__main__":
    if not CWA_API_KEY:
        print("Error：CWA_API_KEY environmental variable is not set!")
        exit(1)

    # Validating API KEY
    if not validate_api_key(CWA_API_KEY):
        print("CWA_API_Key is not valid!")
        exit(1)

    mcp.run()
