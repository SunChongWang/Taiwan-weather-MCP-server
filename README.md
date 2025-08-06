MCP tools that provide the current weather and weather forecasts of Taiwan, and satellite weather images of Taiwan and East Asia
# Taiwan-weather-MCP-server
The server retrieves and transforms the raw weather data from the CWA to the agent that calls the tools. 
## Settings
<pre>
Config = {
        "cwa": {
                 "command": "python",
                 "args": ["path_to_your/server.py","--ui_mode","terminal"],
                 "transport": "stdio",
                 "env": {
                    "CWA_API_KEY": "your_cwa_api_key"
                 }
        }
}</pre>

## Usage
An example demonstrating how a CLI-based MCP client connects to the server:
<pre>
import asyncio
from langchain_community.chat_models import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import AgentType, initialize_agent

llm = ChatOllama(model="qwen3:14b") # or other LLMs

# load the MCP tools
client = MultiServerMCPClient(Config) # the Config is defined above
tools = asyncio.run(client.get_tools())

# create a react agent that has access to the MCP tools
agent = initialize_agent(
    tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# user query
query = "what's the current weather in Taipei?"
response = asyncio.run(agent.ainvoke(query))
</pre>
The tool selected by the LLM returns:
<pre>
```

location: 臺北市
weather summary: 陰時多雲短暫陣雨
probability of precipitation: 40 百分比
outdoor thermal comfort index: 舒適至悶熱
maximum temperature: 31 C
minimum temperature: 27 C

```
</pre>
<pre>
query="give me a 3-day weather forecast of taichung"
</pre>
The tool selected by the agent returns:
<pre>
```text

臺中市
            Temperature    Relative humidity    Wind speed    Probability of precipitation
----------  -------------  -------------------  ------------  ------------------------------
2025-08-03  [28, 26] C     [92, 83] %           [7, 4]        [60, 30] %
2025-08-04  [29, 26] C     [94, 80] %           [5, 3]        [40, 20] %
2025-08-05  [32, 26] C     [91, 78] %           [5, 2]        [50, 20] %
2025-08-06  [32, 25] C     [88, 76] %           [4, 2]        [20, 10] %
2025-08-07  [29, 26] C     [90, 86] %           [3, 2]        [20, 10] %
```
</pre>
<pre>
query="give me a 1-week weather forecast of tainan"
</pre>
The selected tool outputs:
<pre>
```text

臺南市
              T_avg    T_max    T_min    Rel humidity    Wind speed    Rain prob    UV index
----------  -------  -------  -------  --------------  ------------  -----------  ----------
2025-08-03     28       28.5     27.5            91.5           5             70           5
2025-08-04     27.5     28.5     27              90.5           4.5           25           4
2025-08-05     28.5     30       27              88.5           4.5           20           7
2025-08-06     29       30       27              87.5           4.5          nan           6
2025-08-07     29       30       27              87             4            nan           8
2025-08-08     29       30.5     27              86.5           3.5          nan           8
2025-08-09     29       30       27              86             3            nan           8
```
</pre>
<pre>
query="give me an infrared weather image of taiwan"
</pre>
We get a colored ASCII rendering of the infrared satellite image of Taiwan on the terminal:



<img width="1000" height="360" alt="infrared_taiwan" src="https://github.com/user-attachments/assets/8d127229-cb86-47aa-ad05-97e4d7cfb348" />


If the LLM is browser-based and the MCP server is deployed for such a runtime environment through the `--ui_mode browser` in the Config, then the tool outputs a based64 encoded image string of:



![O-C0042-002 (2)](https://github.com/user-attachments/assets/1dc605df-284d-4585-917c-eaa849e5f075)

Note the Arabic numerals in the ASCII rendering represent 'whiteness' of the image - The larger the number, the cloudier the area.
<pre>
query="give me a visible light weather image of taiwan"
</pre>
The chosen tool returns runtime environment compatible rendering of the image:


<img width="1000" height="360" alt="visible_taiwan" src="https://github.com/user-attachments/assets/a5f0c247-e01a-4a66-81cc-6e9e9b9b1909" />


or



![O-C0042-008 (1)](https://github.com/user-attachments/assets/458ecfed-e185-495f-aabf-9e58d3e20690)


<pre>
query="give me a radar reflectivity weather image of taiwan"
</pre>
The tool selected by the terminal-based LLM returns


<img width="1000" height="360" alt="radar_taiwan" src="https://github.com/user-attachments/assets/c4d24672-0afb-4adb-9863-8f4e303e97f0" />


or, if the LLM runs in a web interface,

<img width="720" height="600" alt="O-A0058-003 (1)" src="https://github.com/user-attachments/assets/ca1cb5d2-f644-4c95-8633-b4435a861736" />

In the case of radar reflectivity image, the Arabic numerals in the ASCII rendering represent 'brightness' of the original radar reflectivity RGB image. <br><br>
The CWA also provides weather images of East Asian regions encompassing: Beijing, Chongqing, Hanoi, Ho Chi Minh, Singapore, Brunei, Shenzhen, Hong Kong, Manila, Shanghai, Taipei, Seoul, Osaka, Tokyo, and Sapporo. So, when
<pre>
query="give me an infrared weather image of hong kong"
</pre>
<pre>
query="give me a visible weather image of tokyo"
</pre>
<pre>
query="give me a radar reflectivity weather image of shanghai"
</pre>
the LLM translates user natural language queries to tool callings, getting



<img width="1000" height="360" alt="infrared_ea" src="https://github.com/user-attachments/assets/930d7261-e766-4308-87cc-6c432b4c11f8" />



<img width="1000" height="360" alt="visible_ea" src="https://github.com/user-attachments/assets/c0d03a48-0418-4882-a7d7-f4cb3327d557" />



<img width="1000" height="360" alt="radar_ea" src="https://github.com/user-attachments/assets/53a7bab0-3039-4c80-80b8-d16be8e500ff" />

![O-B0032-002 (2)](https://github.com/user-attachments/assets/78c9aa54-5fd2-4c68-a9fc-cf15fa922ed8)




![O-B0032-001 (2)](https://github.com/user-attachments/assets/4935f342-14b0-42c0-a63f-e39d9217f9ea)







<img width="720" height="600" alt="O-A0058-001" src="https://github.com/user-attachments/assets/8965d982-b2b4-4973-b6a0-a90c86b96c17" />

## Remarks
Note that tool outputs are fed to the LLM for a final response to the user query in almost all agentic AI frameworks, including react agents. This design is OK for readable text outputs as the LLM may further summarize or translate the tool output. However, the image output of our tool is either ANSI escape code or base64-encoded string, which most LLMs were not trained on. Feeding such strings to the LLM for a final response is not productive. A workaround is for the agentic workflow to skip the last step, returning tool output directly to the user. An implementation of such a workflow is shown below:
<pre>
import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient

myConfig = {
        "cwa": {
                 "command": "python",
                 "args": ["d://Python//MCP//CWA//server.py","--ui_mode","terminal"],
                 "transport": "stdio",
                 "env": {
                    "CWA_API_KEY": "CWA-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                 }
        }
}
client = MultiServerMCPClient(myConfig)
tools = asyncio.run(client.get_tools())

llm = ChatOllama(model='gpt-oss:20b') # or other LLMs
llm_with_tools = llm.bind_tools(tools) # A tool calling agent

# a utility to get the tool selected by the LLM in response to user query
get_tool = lambda msg, tools: next((tool for tool in tools if tool.name == msg.tool_calls[0]['name']), None)

# user query
query="give me an infrared weather image of taiwan"

ai_msg = llm_with_tools.invoke(query) # LLM decides which tool to call
selected_tool = get_tool(ai_msg, tools) # identify the tool among the tools

# call the tool 
result = asyncio.run(selected_tool.ainvoke(ai_msg.tool_calls[0])).content

# print out the result
print(result)

# stop here without feeding the result back to LLM
# response = llm_with_tools.invoke(result)
</pre>
Refer to langchain How To for a basic agent workflow https://python.langchain.com/docs/how_to/tool_results_pass_to_model/.

## Tools in Taiwan-weather-MCP-server
Taiwan Weather MCP Server has 3 tools:
* `get_current_weather_conditions(location_name)`: Get the current weather of the specified city/county in Taiwan. Twenty two location names are available: 
            宜蘭, 花蓮, 臺東, 澎湖, 金門, 連江,
            臺北, 新北, 桃園, 臺中, 臺南, 高雄,
            基隆, 新竹縣, 新竹市, 苗栗, 彰化, 南投,
            雲林, 嘉義縣, 嘉義市, 屏東. <br><br>Returns
        a summary of the current weather conditions, including probability of precipitation, outdoor thermal comfort index, and max and min of temperature, of the specified city in Taiwan.

* `get_weather_forecast(location_name, num_days)`: Get 3-day or 1-week weather forecast for the specified city/county in Taiwan. Valid location names include: 
            宜蘭, 花蓮, 臺東, 澎湖, 金門, 連江,
            臺北, 新北, 桃園, 臺中, 臺南, 高雄,
            基隆, 新竹縣, 新竹市, 苗栗, 彰化, 南投,
            雲林, 嘉義縣, 嘉義市, 屏東. <br><br>Returns one of the following tables:

        > A 3-day weather forecast table listing the predicted ranges of temperature, relative humidity, wind speed (Beaufort scale), and probability of precipitation of the specified city in Taiwan over the current and next 3 days.
        > A 7-day weather forecast table listing the predicted temperature (avg, max, and min), relative humidity, wind speed (Beaufort scale), probability of precipitation, and UV index of the specified city in Taiwan over a 7-day period.

* `get_current_weather_image(region, wavelength)`: Get the satellite weather image of Taiwan or East Asia. The imagery updates very 10 minutes. <br><br>Returns
        weather image in a preformatted style based on the runtime environment.

        > If the tool is running in 'terminal' mode, the image is converted to colored ASCII characters and wrapped in a Markdown code block (using triple backticks) to preserve alignment and monospaced formatting.
        > If running in 'browser' mode, the output is wrapped in HTML-safe base64-encoded <img> tags for direct rendering in web-based interfaces.
        > The LLM does not need to infer the runtime environment. Instead, it should display the output according to the provided format. The tool ensures the output is pre-formatted for the intended environment.

## System requirements
* CWA API Key, which can be obtained from a free CWA account (https://opendata.cwa.gov.tw/userLogin)

* python=3.13.2 
* mcp=1.10.1
* requests=2.32.3
* pandas=2.2.3
* tabulate=0.9.0
* pillow=11.0.0 
* matplotlib=3.10.3
