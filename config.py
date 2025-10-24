import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ieeextreme_solutions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    SOLUTIONS_PER_PAGE = 20
    
    # Supported programming languages
    SUPPORTED_LANGUAGES = [
        'Python', 'Java', 'C++', 'C', 'JavaScript', 'TypeScript',
        'Go', 'Rust', 'Ruby', 'PHP', 'C#', 'Kotlin', 'Swift',
        'Scala', 'Haskell', 'R', 'MATLAB', 'Perl', 'Bash'
    ]
