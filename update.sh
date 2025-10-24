#!/bin/bash

echo "🚀 IEEEXtreme Solutions Hub - Update Script"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Stop any running Flask servers
echo "🛑 Stopping any running Flask servers..."
pkill -f "python app.py" 2>/dev/null || true

# Run database migration
echo ""
echo "📦 Running database migration..."
echo "This will add engagement features (likes, comments, leaderboard, etc.)"
python migrate_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Update complete!"
    echo ""
    echo "🎉 NEW FEATURES ADDED:"
    echo "  ❤️  Like and bookmark solutions"
    echo "  💬 Comments system"
    echo "  🏆 Leaderboard with rankings"
    echo "  🔥 Trending solutions page"
    echo "  ⭐ Featured solutions"
    echo "  📊 Time/space complexity tracking"
    echo "  🏷️  Tags and difficulty levels"
    echo ""
    echo "To start the server:"
    echo "  python app.py"
    echo ""
    echo "Then visit: http://localhost:5000"
    echo ""
    echo "Check NEW_FEATURES.md for detailed documentation!"
else
    echo ""
    echo "❌ Update failed. Please check the error messages above."
fi
