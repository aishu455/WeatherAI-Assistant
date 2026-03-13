# Weather AI Assistant - Web Application

A beautiful React-based web application that uses LangChain + Claude AI + OpenWeatherMap to provide intelligent weather information and recommendations.

Built with FastAPI backend for high performance and modern async support.

## 🎯 Features

- **Real-time Weather Data**: Fetches live weather from OpenWeatherMap API
- **AI-Powered Insights**: Claude AI analyzes weather and provides recommendations
- **LangChain Integration**: Uses tool-calling agents for intelligent queries
- **Beautiful UI**: Modern, responsive React interface
- **Chat-like Interface**: Interactive conversation with the AI assistant
- **FastAPI Backend**: Modern, fast, and production-ready
- **Auto API Documentation**: SwaggerUI available at `/docs`

## 📋 Prerequisites

- Python 3.8+
- FastAPI and Uvicorn
- API Keys:
  - OpenWeatherMap API Key (get from https://openweathermap.org/api)
  - Anthropic API Key (get from https://console.anthropic.com/)

## 🚀 Setup Instructions

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install fastapi uvicorn pydantic python-dotenv requests langchain langchain-anthropic langchain-core anthropic
```

### 2. Verify `.env` File

Make sure your `.env` file contains:
```
OPENWEATHERMAP_API_KEY=your-api-key-here
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Start the Backend Server

```bash
python backend.py
```

Output:
```
Starting FastAPI backend on http://localhost:8000
API documentation: http://localhost:8000/docs
```

### 4. Open the Frontend

- Open your browser and go to: `file:///c:/Users/user/OneDrive/Desktop/My Content Journey/Sanchai/index.html`
- Or start a simple HTTP server:

```bash
# Using Python 3
python -m http.server 8001
```

Then visit: `http://localhost:8001`

## 💬 How to Use

1. **Enter a Weather Query** in the input box
   - Example: "What is the weather in Pune?"
   - Or: "What should I wear in Mumbai today?"
   - Or: "Is it going to rain in London?"

2. **Click Send** or press Enter

3. **Wait for AI Response** - Claude will:
   - Fetch real weather data using the `get_weather` tool
   - Analyze the conditions
   - Provide helpful recommendations

4. **View the Response** in the chat interface

## 🏗️ Architecture

### Backend (FastAPI)
- **Base URL**: `http://localhost:8000`
- **Endpoint**: `POST /api/weather`
- **Input**: `{"query": "What is the weather in..."}`
- **Output**: `{"success": true, "query": "...", "response": "..."}`
- **API Docs**: `http://localhost:8000/docs` (SwaggerUI)

### LangChain Components
- **Tool**: `get_weather(city)` - Calls OpenWeatherMap API
- **Model**: Claude Opus 4.1
- **Agent**: Tool-calling agent with system prompt for weather assistance

### Frontend (React)
- Modern UI with gradient background
- Real-time message updates
- Loading state with animated dots
- Error handling and connection status
- Timestamps for each message

## 📁 Files

- `backend.py` - FastAPI server with LangChain agent
- `index.html` - React-based frontend application
- `requirements.txt` - Python dependencies
- `.env` - API keys and configuration
- `README.md` - This file

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure FastAPI is installed
pip install fastapi uvicorn

# Check if port 8000 is already in use
# If so, change the port in backend.py:
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

### CORS errors
- Make sure backend is running on `http://localhost:8000`
- Check that CORS middleware is enabled (it is by default in this version)

### API keys not working
- Verify keys in `.env` file
- Make sure there are no extra spaces
- Restart the backend server

### Access Denied on Windows
If you get permission errors, try running PowerShell as Administrator:
```powershell
python backend.py
```

## 🎨 Features Showcase

- **Gradient UI**: Beautiful purple gradient design
- **Chat Interface**: Messages appear as bubbles (user on right, AI on left)
- **Real-time Updates**: Instant responses using async fetch
- **Loading State**: Animated dots show when Claude is thinking
- **Error Handling**: Clear error messages if something goes wrong
- **Responsive Design**: Works on desktop and mobile devices
- **Auto API Docs**: Interactive API documentation at `/docs`
- **Performance**: FastAPI's async capabilities for better performance

## 🔄 Data Flow

```
User Input (React Frontend)
    ↓
POST /api/weather (HTTP Request)
    ↓
Backend (FastAPI) - Receives Query
    ↓
LangChain Agent
    ↓
Agent decides to use get_weather tool
    ↓
get_weather() calls OpenWeatherMap API
    ↓
Returns live weather data
    ↓
Claude AI analyzes and responds
    ↓
Response sent back to Frontend
    ↓
Displayed in Chat UI
```

## 📝 Example Conversations

**User**: "What is the weather in San Francisco?"
**AI**: Fetches live data, provides temperature, humidity, conditions, and recommends appropriate clothing.

**User**: "Is it raining in London?"
**AI**: Checks London weather and tells you if rain is in the forecast.

**User**: "What should I wear in Tokyo?"
**AI**: Fetches Tokyo weather and provides outfit recommendations based on temperature and conditions.

## 🔗 API Endpoints

### Health Check
```
GET /api/health
```

### Weather Query
```
POST /api/weather
Content-Type: application/json

{
    "query": "What is the weather in Pune?"
}
```

### Interactive API Documentation
Visit `http://localhost:8000/docs` to test endpoints interactively!

---

**Made with ❤️ using React, FastAPI, LangChain, and Claude AI**

