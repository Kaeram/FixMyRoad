# Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended)

1. **Sign up at Railway.app**
   - Visit https://railway.app
   - Sign in with GitHub

2. **Deploy from GitHub**
   ```bash
   # Railway will auto-detect the Python app
   # Create railway.json in project root:
   ```

3. **Set environment variables in Railway dashboard**
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. **Add start command** (if needed)
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

### Option 2: Render

1. **Create account at Render.com**

2. **New Web Service**
   - Connect GitHub repository
   - Choose Python environment

3. **Configure**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port 10000
   ```

4. **Add environment variables**
   - SUPABASE_URL
   - SUPABASE_KEY

### Option 3: Heroku

1. **Install Heroku CLI and login**
   ```bash
   heroku login
   ```

2. **Create Procfile**
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Create runtime.txt**
   ```
   python-3.11.0
   ```

4. **Deploy**
   ```bash
   heroku create fixmyroad-api
   heroku config:set SUPABASE_URL=your_url
   heroku config:set SUPABASE_KEY=your_key
   git push heroku main
   ```

### Option 4: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**
   ```bash
   docker build -t fixmyroad-api .
   docker run -p 8000:8000 -e SUPABASE_URL=your_url -e SUPABASE_KEY=your_key fixmyroad-api
   ```

### Option 5: VPS (Ubuntu)

1. **SSH into server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Clone and setup**
   ```bash
   git clone https://github.com/Kaeram/FixMyRoad.git
   cd FixMyRoad
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create systemd service** (`/etc/systemd/system/fixmyroad.service`)
   ```ini
   [Unit]
   Description=FixMyRoad API
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/FixMyRoad
   Environment="PATH=/path/to/FixMyRoad/venv/bin"
   EnvironmentFile=/path/to/FixMyRoad/.env
   ExecStart=/path/to/FixMyRoad/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Start service**
   ```bash
   sudo systemctl start fixmyroad
   sudo systemctl enable fixmyroad
   ```

6. **Configure Nginx** (`/etc/nginx/sites-available/fixmyroad`)
   ```nginx
   server {
       listen 80;
       server_name api.fixmyroad.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Post-Deployment Checklist

- [ ] Verify API is accessible
- [ ] Test all endpoints with curl/Postman
- [ ] Check database connection
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure CORS for your frontend domain
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure backups for database
- [ ] Set up CI/CD pipeline
- [ ] Add authentication for admin endpoints
- [ ] Enable rate limiting
- [ ] Set up logging aggregation

## Production Environment Variables

Required:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_production_anon_key
APP_NAME=FixMyRoad API
APP_VERSION=1.0.0
DEBUG=False
ML_MODEL_CONFIDENCE_THRESHOLD=0.7
```

Optional (for production features):
```env
SENTRY_DSN=your_sentry_dsn
REDIS_URL=your_redis_url
ADMIN_API_KEY=your_admin_key
RATE_LIMIT_PER_MINUTE=60
```

## Monitoring

### Health Check Endpoint
```bash
curl https://your-api.com/health
```

### Setup uptime monitoring
- Use UptimeRobot, Pingdom, or similar
- Monitor `/health` endpoint every 5 minutes

### Application monitoring
```bash
# Install Sentry
pip install sentry-sdk[fastapi]

# Add to backend/main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use Redis for session management
- Configure connection pooling for database

### Vertical Scaling
- Start with 1GB RAM / 1 CPU
- Monitor resource usage
- Scale up as needed

## Security Hardening

1. **Enable HTTPS only**
2. **Implement rate limiting**
3. **Add API authentication for admin endpoints**
4. **Validate and sanitize all inputs**
5. **Use environment variables for secrets**
6. **Enable CORS only for trusted domains**
7. **Keep dependencies updated**
8. **Regular security audits**

## Troubleshooting

**Problem**: API returns 502 Bad Gateway
- Check if app is running: `systemctl status fixmyroad`
- Check logs: `journalctl -u fixmyroad -f`
- Verify port binding

**Problem**: Database connection fails
- Verify Supabase credentials
- Check network connectivity
- Review Supabase project status

**Problem**: High memory usage
- Enable connection pooling
- Implement caching
- Optimize database queries
