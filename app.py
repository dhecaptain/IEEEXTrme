from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, Solution, Problem, Comment, UserActivity
from config import Config
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from sqlalchemy import func
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Language mapping for Pygments
LANGUAGE_MAP = {
    'Python': 'python',
    'Java': 'java',
    'C++': 'cpp',
    'C': 'c',
    'JavaScript': 'javascript',
    'TypeScript': 'typescript',
    'Go': 'go',
    'Rust': 'rust',
    'Ruby': 'ruby',
    'PHP': 'php',
    'C#': 'csharp',
    'Kotlin': 'kotlin',
    'Swift': 'swift',
    'Scala': 'scala',
    'Haskell': 'haskell',
    'R': 'r',
    'MATLAB': 'matlab',
    'Perl': 'perl',
    'Bash': 'bash'
}

def highlight_code(code, language):
    """Highlight code using Pygments"""
    try:
        lexer_name = LANGUAGE_MAP.get(language, 'text')
        lexer = get_lexer_by_name(lexer_name, stripall=True)
        formatter = HtmlFormatter(style='monokai', linenos=True, cssclass='highlight')
        return highlight(code, lexer, formatter)
    except:
        return f'<pre><code>{code}</code></pre>'

@app.route('/')
def index():
    """Homepage - display all solutions"""
    page = request.args.get('page', 1, type=int)
    language_filter = request.args.get('language', '')
    problem_filter = request.args.get('problem', '')
    search_query = request.args.get('search', '')
    
    # Build query
    query = Solution.query
    
    if language_filter:
        query = query.filter_by(language=language_filter)
    
    if problem_filter:
        query = query.filter_by(problem_name=problem_filter)
    
    if search_query:
        query = query.filter(
            (Solution.problem_name.contains(search_query)) |
            (Solution.description.contains(search_query))
        )
    
    # Order by newest first
    query = query.order_by(Solution.created_at.desc())
    
    # Paginate
    pagination = query.paginate(
        page=page, 
        per_page=app.config['SOLUTIONS_PER_PAGE'],
        error_out=False
    )
    
    solutions = pagination.items
    
    # Get statistics
    total_solutions = Solution.query.count()
    total_problems = Problem.query.count()
    languages_used = db.session.query(Solution.language, func.count(Solution.id))\
        .group_by(Solution.language)\
        .order_by(func.count(Solution.id).desc())\
        .all()
    
    problems_list = db.session.query(Solution.problem_name, func.count(Solution.id))\
        .group_by(Solution.problem_name)\
        .order_by(func.count(Solution.id).desc())\
        .all()
    
    return render_template('index.html',
                         solutions=solutions,
                         pagination=pagination,
                         total_solutions=total_solutions,
                         total_problems=total_problems,
                         languages_used=languages_used,
                         problems_list=problems_list,
                         current_language=language_filter,
                         current_problem=problem_filter,
                         search_query=search_query)

@app.route('/solution/<int:solution_id>')
def view_solution(solution_id):
    """View a single solution with syntax highlighting"""
    solution = Solution.query.get_or_404(solution_id)
    
    # Increment view count
    solution.views += 1
    db.session.commit()
    
    # Highlight code
    highlighted_code = highlight_code(solution.code, solution.language)
    
    # Get CSS for syntax highlighting
    formatter = HtmlFormatter(style='monokai')
    highlight_css = formatter.get_style_defs('.highlight')
    
    # Get other solutions for the same problem
    related_solutions = Solution.query.filter(
        Solution.problem_name == solution.problem_name,
        Solution.id != solution.id
    ).limit(5).all()
    
    return render_template('solution.html',
                         solution=solution,
                         highlighted_code=highlighted_code,
                         highlight_css=highlight_css,
                         related_solutions=related_solutions)

@app.route('/submit', methods=['GET', 'POST'])
def submit_solution():
    """Submit a new solution"""
    if request.method == 'POST':
        problem_name = request.form.get('problem_name', '').strip()
        language = request.form.get('language', '').strip()
        code = request.form.get('code', '').strip()
        author = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        time_complexity = request.form.get('time_complexity', '').strip()
        space_complexity = request.form.get('space_complexity', '').strip()
        tags = request.form.get('tags', '').strip()
        execution_time = request.form.get('execution_time', '').strip()
        
        # Validation
        if not problem_name or not language or not code:
            flash('Please fill in all required fields!', 'error')
            return render_template('submit.html', 
                                 supported_languages=app.config['SUPPORTED_LANGUAGES'])
        
        if language not in app.config['SUPPORTED_LANGUAGES']:
            flash('Invalid programming language!', 'error')
            return render_template('submit.html',
                                 supported_languages=app.config['SUPPORTED_LANGUAGES'])
        
        # Create solution
        solution = Solution(
            problem_name=problem_name,
            language=language,
            code=code,
            author=author if author else None,
            description=description if description else None,
            difficulty=difficulty if difficulty else None,
            time_complexity=time_complexity if time_complexity else None,
            space_complexity=space_complexity if space_complexity else None,
            tags=tags if tags else None,
            execution_time_ms=float(execution_time) if execution_time else None
        )
        
        db.session.add(solution)
        
        # Update or create problem entry
        problem = Problem.query.filter_by(name=problem_name).first()
        if problem:
            problem.solution_count += 1
        else:
            problem = Problem(name=problem_name, solution_count=1)
            db.session.add(problem)
        
        # Update user activity
        if author:
            from models import UserActivity
            user = UserActivity.query.filter_by(username=author).first()
            if user:
                user.solutions_submitted += 1
                user.last_active = datetime.utcnow()
            else:
                user = UserActivity(username=author, solutions_submitted=1)
                db.session.add(user)
        
        db.session.commit()
        
        flash('Solution submitted successfully! 🎉', 'success')
        return redirect(url_for('view_solution', solution_id=solution.id))
    
    return render_template('submit.html',
                         supported_languages=app.config['SUPPORTED_LANGUAGES'])

@app.route('/api/solutions')
def api_solutions():
    """API endpoint to get solutions as JSON"""
    language = request.args.get('language', '')
    problem = request.args.get('problem', '')
    limit = request.args.get('limit', 50, type=int)
    
    query = Solution.query
    
    if language:
        query = query.filter_by(language=language)
    
    if problem:
        query = query.filter_by(problem_name=problem)
    
    solutions = query.order_by(Solution.created_at.desc()).limit(limit).all()
    
    return jsonify([s.to_dict() for s in solutions])

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = {
        'total_solutions': Solution.query.count(),
        'total_problems': Problem.query.count(),
        'languages': [
            {'language': lang, 'count': count}
            for lang, count in db.session.query(
                Solution.language, func.count(Solution.id)
            ).group_by(Solution.language).all()
        ],
        'problems': [
            {'problem': prob, 'count': count}
            for prob, count in db.session.query(
                Solution.problem_name, func.count(Solution.id)
            ).group_by(Solution.problem_name).all()
        ]
    }
    return jsonify(stats)

@app.route('/like/<int:solution_id>', methods=['POST'])
def like_solution(solution_id):
    """Like a solution"""
    solution = Solution.query.get_or_404(solution_id)
    solution.likes += 1
    
    # Update author's activity
    if solution.author:
        user = UserActivity.query.filter_by(username=solution.author).first()
        if user:
            user.total_likes += 1
    
    db.session.commit()
    return jsonify({'success': True, 'likes': solution.likes})


@app.route('/bookmark/<int:solution_id>', methods=['POST'])
def bookmark_solution(solution_id):
    """Bookmark a solution"""
    solution = Solution.query.get_or_404(solution_id)
    solution.bookmarks += 1
    db.session.commit()
    return jsonify({'success': True, 'bookmarks': solution.bookmarks})


@app.route('/comment/<int:solution_id>', methods=['POST'])
def add_comment(solution_id):
    """Add a comment to a solution"""
    solution = Solution.query.get_or_404(solution_id)
    
    author = request.form.get('author', '').strip()
    content = request.form.get('content', '').strip()
    
    if not author or not content:
        flash('Please provide both name and comment!', 'error')
        return redirect(url_for('view_solution', solution_id=solution_id))
    
    comment = Comment(
        solution_id=solution_id,
        author=author,
        content=content
    )
    db.session.add(comment)
    
    # Update user activity
    user = UserActivity.query.filter_by(username=author).first()
    if user:
        user.comments_made += 1
    else:
        user = UserActivity(username=author, comments_made=1)
        db.session.add(user)
    
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('view_solution', solution_id=solution_id))


@app.route('/leaderboard')
def leaderboard():
    """Display user leaderboard"""
    users = UserActivity.query.all()
    # Sort by total score
    sorted_users = sorted(users, key=lambda u: u.total_score, reverse=True)
    
    return render_template('leaderboard.html', users=sorted_users)


@app.route('/trending')
def trending():
    """Show trending solutions (most liked/viewed recently)"""
    from datetime import timedelta
    
    # Solutions from last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    trending_solutions = Solution.query.filter(
        Solution.created_at >= week_ago
    ).order_by(
        (Solution.likes * 5 + Solution.views).desc()
    ).limit(20).all()
    
    return render_template('trending.html', solutions=trending_solutions)


@app.route('/featured')
def featured():
    """Show featured solutions"""
    featured_solutions = Solution.query.filter_by(is_featured=True).order_by(
        Solution.created_at.desc()
    ).all()
    
    return render_template('featured.html', solutions=featured_solutions)


@app.template_filter('format_date')
def format_date(date):
    """Format datetime for display"""
    return date.strftime('%B %d, %Y at %I:%M %p')

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
