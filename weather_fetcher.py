"""
Module providing weather data fetching functionality.
"""
import re
import requests

# List of valid county/city names
VALID_LOCATIONS = ["宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣",
                  "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市",
                  "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣",
                  "雲林縣", "嘉義縣", "嘉義市", "屏東縣"]

# CWA API endpoints
THREE_DAYS_FORECAST_ENDPOINT = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089"
ONE_WEEK_FORECAST_ENDPOINT = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091"
THIRTYSIX_HOURS_FORECAST_ENDPOINT = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

def fetch_three_days_forecast(location, api_key):
    """Fetch 3-day weather forecast data from CWA API
    
    Args:
        location: County/city name
        api_key: API key
        
    Returns:
        dict: Raw weather data
        
    Raises:
        Exception: If API request fails or errors occur
    """
    url = THREE_DAYS_FORECAST_ENDPOINT
    params = {
        "Authorization": api_key,
        "LocationName": location
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed, status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching weather data: {str(e)}")


def fetch_one_week_forecast(location, api_key):
    """Fetch 1-week weather forecast data from CWA API
    
    Args:
        location: County/city name
        api_key: API key
        
    Returns:
        dict: Raw weather data
        
    Raises:
        Exception: If API request fails or errors occur
    """
    url = ONE_WEEK_FORECAST_ENDPOINT
    params = {
        "Authorization": api_key,
        "LocationName": location
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed, status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching weather data: {str(e)}")


def fetch_thirtySix_hours_forecast(location, api_key):
    """Fetch 36-hour weather forecast data from CWA API
    
    Args:
        location: County/city name
        api_key: API key
        
    Returns:
        dict: Raw weather data
        
    Raises:
        Exception: If API request fails or errors occur
    """
    url = THIRTYSIX_HOURS_FORECAST_ENDPOINT
    params = {
        "Authorization": api_key,
        "locationName": location
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed, status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching weather data: {str(e)}")


def get_valid_location(input_location):
    # 將訊息中的 "台" 替換為 "臺"
    corrected_location = re.sub("台", "臺", input_location)

    for L in VALID_LOCATIONS:
        if re.search(corrected_location, L):
            return L

    if corrected_location not in VALID_LOCATIONS:
        valid_locations_str = ", ".join(VALID_LOCATIONS)
        raise ValueError(f"Invalid location name. Valid location names are: {valid_locations_str}")

    # default location
    return "臺北市"


def validate_api_key(api_key: str) -> bool:
    """
    validity of the CWA API KEY

    Args:
        api_key (str): CWA API KEY

    Returns:
        bool: True if valid, False otherwise 
    """
    # testing the validity
    try:
        test_url = THREE_DAYS_FORECAST_ENDPOINT
        params = {
            "Authorization": api_key,
            "LocationName": "臺北市"
        }

        response = requests.get(test_url, params=params)

        # HTTP status code
        if response.status_code == 200:
            return True

        # 401 Unauthorized
        elif response.status_code == 401:
            print(f"API Key failure: {response.text}")
            return False

    except Exception as e:
        print(f"API Key error: {str(e)}")
        return False
