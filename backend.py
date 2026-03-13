import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(override=True)

app = FastAPI(title="Weather AI Assistant API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherQuery(BaseModel):
    query: str

class WeatherResponse(BaseModel):
    success: bool
    query: str = None
    response: str = None
    error: str = None

@tool
def get_weather(city: str) -> str:
    """Get real live weather for a given city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if not api_key:
        return "Error: OPENWEATHERMAP_API_KEY not found"
    
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
            
            return f"Weather in {city}: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%, Conditions: {description}, Wind: {wind_speed} m/s"
        else:
            return f"Error: {response.json().get('message', 'City not found')}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_agent():
    """Create and return a LangChain agent."""
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env")
    
    model = ChatAnthropic(model="claude-opus-4-1", api_key=anthropic_api_key)
    tools = [get_weather]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful weather assistant. Use the get_weather tool to fetch real weather data. Provide helpful recommendations based on the weather."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "Backend is running", "service": "Weather AI Assistant API"}

@app.post("/api/weather", response_model=WeatherResponse)
async def weather_query(weather_query: WeatherQuery):
    """Handle weather queries from the frontend."""
    try:
        user_query = weather_query.query.strip()
        
        if not user_query:
            return WeatherResponse(
                success=False,
                error="Query cannot be empty"
            )
        
        agent_executor = get_agent()
        result = agent_executor.invoke({"input": user_query})
        
        response_text = result.get('output', 'No response')
        
        # Clean up response if it's a list (from LangChain)
        if isinstance(response_text, list):
            response_text = response_text[0].get('text', 'No response') if response_text else 'No response'
        
        return WeatherResponse(
            success=True,
            query=user_query,
            response=response_text
        )
    
    except Exception as e:
        return WeatherResponse(
            success=False,
            error=str(e)
        )

if __name__ == '__main__':
    import uvicorn
    print("Starting FastAPI backend on http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
