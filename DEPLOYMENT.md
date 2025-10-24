# Deployment Guide - IEEEXtreme Solutions Hub

This guide covers multiple deployment options for your IEEEXtreme Solutions Hub.

## Option 1: PythonAnywhere (Easiest - Free Tier Available)

PythonAnywhere is perfect for Python web apps and offers a free tier.

### Steps:

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your files**:
   - Use the "Files" tab to upload all project files
   - Or clone from Git: `git clone <your-repo-url>`

3. **Install dependencies**:
   - Open a Bash console
   - Navigate to your project directory
   - Create virtual environment: `mkvirtualenv --python=/usr/bin/python3.10 ieeextreme`
   - Install: `pip install -r requirements.txt`

4. **Initialize database**:
   ```bash
   python init_db.py
   ```

5. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" with Python 3.10
   - Set source code directory: `/home/yourusername/IEE`
   - Set working directory: `/home/yourusername/IEE`

6. **Configure WSGI file**:
   Edit the WSGI configuration file:
   ```python
   import sys
   path = '/home/yourusername/IEE'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

7. **Reload** your web app and visit `yourusername.pythonanywhere.com`

---

## Option 2: Heroku

### Prerequisites:
- Heroku account
- Heroku CLI installed
- Git repository

### Steps:

1. **Add these files to your project**:

Create `Procfile`:
```
web: gunicorn app:app
```

Update `requirements.txt` to include:
```
gunicorn==21.2.0
```

2. **Deploy**:
```bash
heroku login
heroku create ieeextreme-solutions
git push heroku main
heroku run python init_db.py
heroku open
```

3. **Set environment variables**:
```bash
heroku config:set SECRET_KEY='your-secret-key-here'
```

---

## Option 3: Railway.app

Railway offers free hosting with automatic deployments.

### Steps:

1. **Sign up** at [railway.app](https://railway.app)

2. **New Project** → "Deploy from GitHub repo"

3. **Select your repository**

4. **Configure**:
   - Start command: `python app.py`
   - Add environment variables if needed

5. **Deploy** - Automatic on every git push!

---

## Option 4: Render.com

### Steps:

1. **Sign up** at [render.com](https://render.com)

2. **New Web Service** → Connect your GitHub repo

3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

4. **Add environment variables** in dashboard

5. **Deploy**!

---

## Option 5: DigitalOcean App Platform

### Steps:

1. **Sign up** at [digitalocean.com](https://www.digitalocean.com)

2. **Create App** → Select your GitHub repo

3. **Configure**:
   - Environment: Python
   - Run Command: `python app.py`

4. **Deploy** - $5/month after free trial

---

## Option 6: Self-Hosted (VPS)

For full control, deploy on a VPS (AWS EC2, DigitalOcean Droplet, etc.)

### Quick Setup:

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone your repo
git clone <your-repo>
cd IEE

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Initialize database
python init_db.py

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

### Setup Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Environment Variables

For production, set these environment variables:

- `SECRET_KEY`: A random secret key for Flask sessions
- `DATABASE_URL`: (Optional) PostgreSQL database URL for production

---

## Post-Deployment Checklist

- ✅ Test solution submission
- ✅ Test solution viewing
- ✅ Test search and filters
- ✅ Verify syntax highlighting works
- ✅ Check mobile responsiveness
- ✅ Set up custom domain (optional)
- ✅ Enable HTTPS (most platforms do this automatically)

---

## Scaling Tips

1. **Database**: Migrate from SQLite to PostgreSQL for better performance
2. **Caching**: Add Redis for caching popular solutions
3. **CDN**: Use Cloudflare for static assets
4. **Monitoring**: Add application monitoring (Sentry, New Relic)

---

## Support

For issues or questions, check the README.md or create an issue in your repository.
