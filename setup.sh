#!/bin/bash

# ResumeBoost AI - Setup Script

set -e

echo "🚀 ResumeBoost AI - Setup Script"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=$(openssl rand -hex 32)
EOF
    echo "✅ .env file created. Please update OPENAI_API_KEY with your actual key."
else
    echo "✅ .env file already exists."
fi

# Create backend .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/.env.example backend/.env
    echo "✅ backend/.env file created."
else
    echo "✅ backend/.env file already exists."
fi

# Build images
echo ""
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for backend to be ready
echo ""
echo "⏳ Waiting for backend to be ready..."
sleep 10

# Check if backend is healthy
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is ready!"
else
    echo "⚠️  Backend might still be starting. Check logs with: docker-compose logs backend"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"
echo ""
