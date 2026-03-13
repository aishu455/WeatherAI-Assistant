import os
import requests
import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(override=True)

@tool
def get_weather(city: str) -> str:
    """
    Get real live weather for a given city using OpenWeatherMap API.
    
    Args:
        city: The name of the city
    
    Returns:
        A string with weather information including temperature, humidity, and conditions
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if not api_key:
        return "Error: OPENWEATHERMAP_API_KEY not found in environment"
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            weather_info = f"""
Weather in {city}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Humidity: {humidity}%
- Conditions: {description}
- Wind Speed: {wind_speed} m/s
"""
            return weather_info
        else:
            error_msg = response.json().get('message', 'Unknown error')
            return f"Error fetching weather for {city}: {error_msg}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not anthropic_api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env file")
        exit(1)
    
    print("Initializing LangChain Weather Agent...")
    print("="*60)
    
    model = ChatAnthropic(model="claude-opus-4-1", api_key=anthropic_api_key)
    
    tools = [get_weather]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful weather assistant. Use the get_weather tool to fetch real weather data for cities. Provide helpful weather information and recommendations based on the current conditions."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    print("\nAsking agent: 'What is the weather in Pune?'")
    print("="*60)
    
    result = agent_executor.invoke(
        {"input": "What is the weather in Pune,India?"}
    )
    
    print("\n" + "="*60)
    print("[FINAL RESPONSE]")
    print(result["output"])

if __name__ == "__main__":
    main()
