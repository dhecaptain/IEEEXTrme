# IEEEXtreme Solutions Hub 🏆

A web platform for sharing and browsing 100% solutions from IEEEXtreme programming competition.

## Features

- ✅ Submit solutions with code, problem name, and programming language
- 🔍 Browse and search solutions by problem or language
- 🎨 Syntax highlighting for 19+ programming languages
- 📊 Statistics and solution counts
- 🚀 Fast and lightweight SQLite database
- 📱 Responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd /home/david/Documents/IEE
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment**
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Initialize the database**
```bash
python init_db.py
```

6. **Run the application**
```bash
python app.py
```

7. **Open your browser**
Navigate to: `http://localhost:5000`

## Usage

### Submit a Solution
1. Click "Submit Solution" in the navigation
2. Enter the problem name (e.g., "Two Sum", "Binary Search")
3. Select your programming language
4. Paste your code
5. Optionally, add your name/username
6. Submit!

### Browse Solutions
- View all solutions on the homepage
- Filter by problem name or programming language
- Use the search bar to find specific solutions
- Click on solutions to see full code with syntax highlighting

## Project Structure

```
IEE/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── init_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── submit.html       # Submit solution form
│   └── solution.html     # View single solution
├── static/               # Static files (CSS, JS)
│   └── style.css         # Stylesheet
└── README.md             # This file
```

## Deployment

### Deploy to PythonAnywhere (Free)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Set up a web app with Flask
4. Configure WSGI file to point to `app.py`

### Deploy to Heroku
1. Install Heroku CLI
2. Create `Procfile`: `web: python app.py`
3. Add `gunicorn` to requirements.txt
4. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to Railway/Render
- Connect your GitHub repository
- Set start command: `python app.py`
- Deploy automatically on push

## Contributing

This project is for the IEEEXtreme community. To contribute:
1. Solve a problem and get 100%
2. Submit your solution via the web interface
3. Help others learn from your approach!

## License

Open source - feel free to use and modify for your team or university!

## Notes

- Only submit solutions that scored 100%
- Respect the IEEEXtreme code of conduct
- Share solutions AFTER the competition ends
- Be respectful and supportive of all skill levels

---

Built with ❤️ for the IEEEXtreme community
