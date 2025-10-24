# Architecture & Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER'S BROWSER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Homepage   │  │    Submit    │  │   Solution   │     │
│  │              │  │     Form     │  │    Viewer    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           ↕ HTTP
┌─────────────────────────────────────────────────────────────┐
│                   FLASK WEB SERVER                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes (app.py)                                     │  │
│  │  • GET  /              → Show all solutions          │  │
│  │  • GET  /solution/<id> → View one solution           │  │
│  │  • GET  /submit        → Show submit form            │  │
│  │  • POST /submit        → Save new solution           │  │
│  │  • GET  /api/solutions → JSON API                    │  │
│  │  • GET  /api/stats     → Statistics API              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic                                      │  │
│  │  • Syntax highlighting (Pygments)                    │  │
│  │  • Search & filtering                                │  │
│  │  • Pagination                                        │  │
│  │  • Validation                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Models (models.py)                                  │  │
│  │  • Solution model                                    │  │
│  │  • Problem model                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────┐
│                  SQLite DATABASE                            │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │  solutions table    │    │  problems table     │        │
│  ├─────────────────────┤    ├─────────────────────┤        │
│  │ id                  │    │ id                  │        │
│  │ problem_name        │    │ name                │        │
│  │ language            │    │ solution_count      │        │
│  │ code                │    └─────────────────────┘        │
│  │ author              │                                    │
│  │ description         │                                    │
│  │ created_at          │                                    │
│  │ views               │                                    │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Viewing Solutions (GET /)

```
User Browser
    ↓
  [GET /]
    ↓
Flask Route (index)
    ↓
Query Database
    ↓
Apply Filters & Pagination
    ↓
Render Template (index.html)
    ↓
Return HTML + CSS
    ↓
User sees solutions grid
```

### 2. Submitting Solution (POST /submit)

```
User fills form
    ↓
[POST /submit]
    ↓
Flask Route (submit_solution)
    ↓
Validate Input
    ↓
Create Solution object
    ↓
Save to Database
    ↓
Update Problem count
    ↓
Redirect to solution view
    ↓
User sees their solution
```

### 3. Viewing Single Solution (GET /solution/1)

```
User clicks solution
    ↓
[GET /solution/1]
    ↓
Flask Route (view_solution)
    ↓
Fetch from Database
    ↓
Increment view count
    ↓
Apply Syntax Highlighting (Pygments)
    ↓
Find Related Solutions
    ↓
Render Template (solution.html)
    ↓
User sees highlighted code
```

## Component Interaction

```
┌────────────────────────────────────────────────┐
│              PRESENTATION LAYER                │
│                                                 │
│  Templates/                                     │
│  ├── base.html      (Navigation, footer)       │
│  ├── index.html     (Solutions grid)           │
│  ├── submit.html    (Form)                     │
│  └── solution.html  (Code viewer)              │
│                                                 │
│  Static/                                        │
│  └── style.css      (Styling)                  │
└────────────────────────────────────────────────┘
                     ↕
┌────────────────────────────────────────────────┐
│              APPLICATION LAYER                 │
│                                                 │
│  app.py                                        │
│  ├── Routes (URL handling)                    │
│  ├── Request processing                       │
│  ├── Response formatting                      │
│  └── Template rendering                       │
│                                                 │
│  config.py                                     │
│  └── Configuration settings                   │
└────────────────────────────────────────────────┘
                     ↕
┌────────────────────────────────────────────────┐
│               DATA ACCESS LAYER                │
│                                                 │
│  models.py                                     │
│  ├── Solution (ORM model)                     │
│  │   ├── Fields definition                    │
│  │   └── Methods (to_dict)                    │
│  └── Problem (ORM model)                      │
│      ├── Fields definition                    │
│      └── Relationships                        │
└────────────────────────────────────────────────┘
                     ↕
┌────────────────────────────────────────────────┐
│               DATABASE LAYER                   │
│                                                 │
│  ieeextreme_solutions.db (SQLite)             │
│  ├── solutions table                          │
│  └── problems table                           │
└────────────────────────────────────────────────┘
```

## Request/Response Cycle

### Example: User Searches for Python Solutions

```
1. User Input
   └─> Browser: Click filter "Python"
   
2. HTTP Request
   └─> GET /?language=Python
   
3. Flask Processing
   ├─> Route: index()
   ├─> Extract: language_filter = 'Python'
   ├─> Query: Solution.query.filter_by(language='Python')
   ├─> Execute: Database query
   └─> Paginate: Results
   
4. Template Rendering
   ├─> Load: templates/index.html
   ├─> Inject: solutions, filters, stats
   └─> Render: HTML with data
   
5. HTTP Response
   └─> Return: HTML + CSS
   
6. Browser Display
   └─> Show: Filtered solutions grid
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│          Frontend (Browser)             │
│  • HTML5                                │
│  • CSS3 (Custom, responsive)            │
│  • JavaScript (Vanilla, minimal)        │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│         Backend (Flask Server)          │
│  • Flask 3.0 (Web framework)            │
│  • Jinja2 (Template engine)             │
│  • Werkzeug (WSGI toolkit)              │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│      ORM (Database Abstraction)         │
│  • SQLAlchemy (ORM)                     │
│  • Flask-SQLAlchemy (Integration)       │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│         Database (Storage)              │
│  • SQLite (File-based DB)               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      Utilities (Helper Libraries)       │
│  • Pygments (Syntax highlighting)       │
└─────────────────────────────────────────┘
```

## File Dependencies

```
app.py
  ├─ imports models.py
  │    └─ defines Solution, Problem
  ├─ imports config.py
  │    └─ provides Config class
  └─ uses templates/
       ├─ base.html
       ├─ index.html
       ├─ submit.html
       └─ solution.html
            └─ include static/style.css

init_db.py
  ├─ imports app.py
  └─ imports models.py
       └─ creates database tables
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│            Users/Browsers               │
└─────────────────────────────────────────┘
                  ↓ HTTPS
┌─────────────────────────────────────────┐
│        Hosting Platform (Choose)        │
│  • PythonAnywhere / Heroku / Railway   │
│  • Render / DigitalOcean / VPS         │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Web Server/WSGI                │
│  • Gunicorn (production)                │
│  • Flask dev server (development)       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Your Flask Application          │
│  (All the code you created)             │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Database File                  │
│  ieeextreme_solutions.db                │
└─────────────────────────────────────────┘
```

---

This architecture is:
- ✅ **Simple** - Easy to understand and modify
- ✅ **Scalable** - Can grow with more features
- ✅ **Maintainable** - Clean separation of concerns
- ✅ **Deployable** - Works on many platforms
- ✅ **Secure** - Input validation, CSRF protection
