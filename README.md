# NASA Manufacturing Intelligence Dashboard

A comprehensive production management system with AI-powered chat assistance, real-time cost/time estimation, and weather-integrated production simulation.

## 🚀 Features

- **Product Management**: Complete NASA product catalog with detailed specifications
- **Production Breakdown**: Step-by-step manufacturing process visualization
- **Estimation Tools**: Real-time cost and time calculations
- **Production Simulation**: Date-based planning with weather forecasting
- **AI Chat Assistant**: CrewAI-powered conversational interface
- **Premium Dashboard**: Modern, responsive web interface

## 📋 Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **MongoDB** (local or cloud instance)
- **Git**

## 🛠️ Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd HackATL2025
```

### 2. Backend Setup (FastAPI + Python)

#### Install Python Dependencies
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi uvicorn motor pymongo python-dotenv requests crewai crewai-tools pydantic
```

#### Environment Configuration
```bash
# Create .env file in root directory
cp .env.example .env
```

Edit `.env` file with your MongoDB and OPENAI_API_KEY credentials:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=your_database_name

OPENAI_API_KEY=your_openai_api_key
```

#### Database Setup
```bash
# Seed the database with sample data
python seed_data.py
```

#### Start Backend Server
```bash
uvicorn app.main:app --reload
```
Backend will run on: `http://localhost:8000`

### 3. Frontend Setup (Next.js + React)

#### Navigate to Frontend Directory
```bash
cd hackatl-dashboard
```

#### Install Dependencies
```bash
npm install
```

#### Start Frontend Server
```bash
npm run dev
```
Frontend will run on: `http://localhost:3000`

## 🔧 Project Structure

```
HackATL2025/
├── app/                          # Backend (FastAPI)
│   ├── routes/                   # API endpoints
│   │   ├── product.py           # Product management APIs
│   │   ├── chatbot.py           # AI chat interface
│   │   └── simulation.py        # Production simulation
│   ├── agents/                   # CrewAI agents
│   ├── tools/                    # AI tools for data fetching
│   ├── crews/                    # AI crew coordination
│   ├── database.py              # MongoDB connection
│   └── main.py                  # FastAPI application
├── hackatl-dashboard/           # Frontend (Next.js)
│   ├── app/
│   │   ├── page.tsx            # Main dashboard component
│   │   ├── layout.tsx          # App layout
│   │   └── globals.css         # Global styles
│   └── package.json            # Frontend dependencies
├── seed_data.py                # Database seeding script
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🚀 Usage

### 1. Access Dashboard
Open `http://localhost:3000` in your browser

### 2. Available Features
- **Products**: View NASA product catalog
- **Production Breakdown**: Analyze manufacturing steps
- **Estimation Tool**: Calculate time and cost estimates
- **Run Simulation**: Plan production with weather forecasting
- **Chat Assistant**: Ask questions about products and processes

### 3. API Endpoints
- `GET /product` - List all products
- `GET /production-step/{product_id}` - Get production steps
- `GET /estimate/time/{product_id}` - Get time estimate
- `GET /estimate/cost/{product_id}` - Get cost estimate
- `POST /simulate` - Run production simulation
- `POST /chat` - Chat with AI assistant

## 🔍 Troubleshooting

### Backend Issues
```bash
# Check if MongoDB is connected
curl http://localhost:8000/product

# Restart backend server
uvicorn app.main:app --reload
```

### Frontend Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database Issues
```bash
# Re-seed database
python seed_data.py
```

## 🛡️ Environment Variables

Create `.env` file with:
```env
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=your_database_name
```

## 📦 Dependencies

### Backend
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `motor` - Async MongoDB driver
- `pymongo` - MongoDB driver
- `crewai` - AI agent framework
- `requests` - HTTP client
- `pydantic` - Data validation

### Frontend
- `next` - React framework
- `react` - UI library
- `typescript` - Type safety
- `tailwindcss` - CSS framework

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify MongoDB connection
4. Check that both servers are running on correct ports

For additional help, create an issue in the repository.
