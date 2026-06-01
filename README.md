# Hobbyist AI - Professional Hobby Recommendation App

## 🎯 Overview

Hobbyist AI uses **Strands Agents** framework to provide personalized hobby recommendations through intelligent orchestration of multiple AI agents. The app combines:

- **Strands Agents**: Advanced agent orchestration framework (invented for this project)
- **FastAPI**: Modern Python web framework
- **AI Models**: Personality analysis, activity recommendation, and scheduling AI
- **Public APIs**: Integration with Meetup, Eventbrite, Reddit for real event data
- **React/Vite**: Modern frontend with real-time updates

## 📁 Project Structure

```
hobbyist/
├── backend/                # Python/FastAPI backend
│   ├── agents/             # Strands Agents orchestration
│   ├── middleware/         # API aggregators and services
│   ├── models/             # Pydantic models
│   ├── routes/             # API endpoints
│   ├── utils/              # Utilities and helpers
│   ├── main.py            # FastAPI app entry point
│   ├── strands_agent_framework.py  # Strands Agent utilities
│   ├── uvicorn.py         # Server configuration
│   ├── pyproject.toml     # Python dependencies
│   └── README.md
├── frontend/               # React/Vite frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── pages/         # Page components
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── vite.config.js
│   └── package.json
└── pyproject.toml         # Root dependencies (if needed)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- git

### Backend Setup

```bash
cd hobbyist/backend

# Install dependencies
pip install -e .

# Run with Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Run Together

Terminal 1: `backend`
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Terminal 2: `frontend`
```bash
cd frontend
npm run dev
```

Then visit: http://localhost:3000

## 🧠 How It Works

1. **User Registration**: User fills out interests and MBTI quiz
2. **Agent Analysis**: Profile Agents analyze personality and preferences
3. **Activity Discovery**: Event Agents fetch activities from public APIs
4. **Orchestration**: Strands Agents orchestrate recommendations
5. **Personalization**: Schedule Agent creates personalized plan
6. **Insights**: Insight Agent provides personalized guidance

## 🛠️ Strands Agents Framework

The proprietary **Strands Agents** framework we invented:

- **Multi-Agent System**: Coordinate multiple specialized agents
- **Context Management**: Share state between agents
- **Orchestration**: Intelligent workflow management
- **Flexibility**: Easy to add new agent types

### Available Agents

- **ProfileAgent**: Analyzes user profile
- **AnalysisAgent**: Analyzes personality and interests
- **DiscoveryAgent**: Fetches activities from APIs
- **RecommendationAgent**: Generates activity suggestions
- **SchedulerAgent**: Creates organized schedules
- **InsightAgent**: Provides personalized feedback

## 🔌 API Endpoints

### User Management

- `GET /api/users/{email}` - Get user profile
- `POST /api/users/register` - Register new user
- `POST /api/users/{email}/profile` - Update profile

### Recommendations

- `GET /api/recommendations/{email}` - Get recommendations
- `POST /api/recommendations/weekly-plan/{email}` - Generate weekly plan
- `GET /api/recommendations/{email}/progress/{week}` - Get progress
- `POST /api/recommendations/complete/{email}/{activity_id}` - Mark complete

### Search & Browse

- `GET /api/search/hobbies` - Search hobbies
- `GET /api/trending` - Get popular hobbies
- `GET /api/categories` - List all hobby categories

## 🎨 Frontend Features

- **Get Started**: Welcome page with features
- **Interest Form**: Profile quiz with MBTI assessment
- **Dashboard**: Real-time hobby plans and recommendations

## 🔐 Security

- Pydantic models for input validation
- CORS middleware configured
- API-based authentication (implement OAuth2 when ready)

## 📊 Technologies Used

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | React 18, Vite |
| **Agents** | Strands Agents (Custom) |
| **Validation** | Pydantic |
| **Database** | SQLite (with PostgreSQL ready) |
| **APIs** | Eventbrite, Meetup, Reddit |

## 🧩 Strands Agent Integration

The app integrates with Strands Agents through:

- **Orchestration Layer**: `agents/orchestrator.py`
- **Agent Context**: Shared state management
- **Agent Communication**: Message passing via context

## 🐛 Development

### Run Tests

```bash
# Backend tests
pytest tests/

# Frontend tests
npm test
```

### Code Quality

```bash
# Backend linting
ruff check backend/
mypy backend/

# Frontend linting
npm run lint
```

## 🚀 Deployment

### Production Build

```bash
# Backend
pip install -e .[prod]
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend
npm run build
# Deploy dist/ to CDN
```

### Environment Variables

Create `.env` file:

```bash
DATABASE_URL=sqlite:///./hobbyist.db
API_KEY=eventbrite_demo_key
MEETUP_API_KEY=your_meetup_key
REDDIT_CLIENT_ID=your_reddit_client_id
SECRET_KEY=your_secret_key
```

## 📈 Metrics & Monitoring

- Request counts per endpoint
- Response times
- Agent execution statistics
- User engagement analytics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📜 License

MIT License

## 👥 Team

Built with ❤️ by the Hobbyist AI team

## 📞 Support

- Issues: [GitHub Issues](issues)
- Email: support@hobbyist.ai

---

Built with **Strands Agents** and **FastAPI** 🚀