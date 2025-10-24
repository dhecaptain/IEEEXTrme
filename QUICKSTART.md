# Quick Reference Guide

## Project Overview

**IEEEXtreme Solutions Hub** is a web platform for sharing 100% solutions from IEEEXtreme competitions.

## File Structure

```
IEE/
├── app.py                    # Main Flask application (routes, logic)
├── models.py                 # Database models (Solution, Problem)
├── config.py                 # App configuration
├── init_db.py                # Database initialization script
├── requirements.txt          # Python dependencies
├── start.sh                  # Quick start script (Linux/Mac)
├── Procfile                  # Heroku deployment config
├── .gitignore               # Git ignore rules
├── README.md                 # Main documentation
├── DEPLOYMENT.md             # Deployment guide
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Homepage
│   ├── submit.html          # Submit form
│   └── solution.html        # Solution detail view
└── static/                  # Static files
    └── style.css            # Stylesheet
```

## Common Commands

### First Time Setup
```bash
# Linux/Mac
./start.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

### Running the App
```bash
source venv/bin/activate  # Activate virtual environment
python app.py             # Start the server
```

Visit: http://localhost:5000

### Database Operations
```bash
# Initialize fresh database
python init_db.py

# Reset database (delete and recreate)
rm -f ieeextreme_solutions.db
python init_db.py
```

## API Endpoints

### Web Routes
- `GET /` - Homepage with all solutions
- `GET /solution/<id>` - View specific solution
- `GET /submit` - Submit solution form
- `POST /submit` - Handle solution submission

### API Routes (JSON)
- `GET /api/solutions?language=Python&problem=Two+Sum&limit=50` - Get solutions as JSON
- `GET /api/stats` - Get statistics

## Database Schema

### Solution Table
- `id` - Primary key
- `problem_name` - Name of the problem
- `language` - Programming language
- `code` - Solution code
- `author` - Author name (optional)
- `description` - Explanation (optional)
- `created_at` - Timestamp
- `views` - View count

### Problem Table
- `id` - Primary key
- `name` - Problem name
- `solution_count` - Number of solutions

## Features

✅ Submit solutions (code + metadata)
✅ Browse all solutions
✅ Filter by language or problem
✅ Search functionality
✅ Syntax highlighting (19+ languages)
✅ View counter
✅ Related solutions
✅ Responsive design
✅ RESTful API

## Customization

### Add More Languages
Edit `config.py` → `SUPPORTED_LANGUAGES`

### Change Styling
Edit `static/style.css`

### Modify Templates
Edit files in `templates/`

### Change Database
Edit `config.py` → `SQLALCHEMY_DATABASE_URI`

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Database Locked Error
- Close all connections
- Delete `ieeextreme_solutions.db`
- Run `python init_db.py`

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Syntax Highlighting Not Working
- Check `Pygments` is installed: `pip show pygments`
- Verify language name in `LANGUAGE_MAP` (app.py)

## Tips

1. **Before Competition**: Set up the platform
2. **During Competition**: Focus on solving problems!
3. **After Competition**: Share your 100% solutions
4. **Always**: Be respectful and follow IEEEXtreme rules

## Contributing Solutions

1. Go to `/submit`
2. Fill in:
   - Problem name (exact)
   - Programming language
   - Your code
   - Optional: Description, your name
3. Submit!
4. Share the link with your team

## Security Notes

- Change `SECRET_KEY` in production
- Don't share database file
- Review submissions if needed
- Consider adding moderation

## Performance Tips

- Use PostgreSQL for production
- Add caching (Redis)
- Enable gzip compression
- Use CDN for static files

## License

Open source - modify as needed for your team!

---

**Need Help?** Check README.md or DEPLOYMENT.md
