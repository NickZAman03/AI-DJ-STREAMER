# 🚀 Deployment Guide - AI DJ Streamer

This guide will help you deploy your AI DJ Streamer to various hosting platforms.

## 🎯 **Option 1: Render (Recommended - Free & Easy)**

### Step 1: Prepare Your Repository
1. Make sure your code is pushed to GitHub
2. Ensure all files are committed:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `ai-dj-streamer`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=$PORT)"`
5. Add Environment Variables:
   - `CONFLUENT_BOOTSTRAP_SERVERS`: Your Kafka cluster URL
   - `CONFLUENT_API_KEY`: Your Confluent API key
   - `CONFLUENT_API_SECRET`: Your Confluent API secret
   - `KAFKA_TOPIC`: `live-chat`
6. Click "Create Web Service"

### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.onrender.com`
- The first deployment may take 5-10 minutes

---

## 🎯 **Option 2: Railway**

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python app
5. Add environment variables in the Railway dashboard
6. Deploy!

---

## 🎯 **Option 3: Heroku**

### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set CONFLUENT_BOOTSTRAP_SERVERS="your-kafka-url"
heroku config:set CONFLUENT_API_KEY="your-api-key"
heroku config:set CONFLUENT_API_SECRET="your-api-secret"
heroku config:set KAFKA_TOPIC="live-chat"

# Deploy
git push heroku main

# Open the app
heroku open
```

---

## 🎯 **Option 4: Vercel (Frontend Only)**

### Step 1: Deploy Frontend
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will automatically detect it's a static site
4. Deploy!

**Note**: This will only host the frontend. You'll need to deploy the backend separately.

---

## 🔧 **Environment Variables Setup**

### Required Variables
```bash
CONFLUENT_BOOTSTRAP_SERVERS=your-cluster.confluent.cloud:9092
CONFLUENT_API_KEY=your-api-key
CONFLUENT_API_SECRET=your-api-secret
KAFKA_TOPIC=live-chat
```

### Optional Variables
```bash
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🐳 **Docker Deployment**

### Local Docker
```bash
# Build the image
docker build -t ai-dj-streamer .

# Run the container
docker run -p 8000:8000 -e CONFLUENT_BOOTSTRAP_SERVERS="your-url" -e CONFLUENT_API_KEY="your-key" -e CONFLUENT_API_SECRET="your-secret" ai-dj-streamer
```

### Docker Compose
```bash
# Create .env file with your variables
cp env.example .env
# Edit .env with your actual values

# Deploy
docker-compose up -d
```

---

## 🌐 **Custom Domain Setup**

### Render
1. Go to your service dashboard
2. Click "Settings" → "Custom Domains"
3. Add your domain
4. Update DNS records as instructed

### Heroku
```bash
heroku domains:add yourdomain.com
# Follow the DNS configuration instructions
```

---

## 📊 **Monitoring & Logs**

### Render
- View logs in the service dashboard
- Set up alerts for downtime

### Heroku
```bash
# View logs
heroku logs --tail

# Monitor dyno usage
heroku ps
```

---

## 🔒 **Security Considerations**

1. **Environment Variables**: Never commit sensitive data
2. **HTTPS**: All platforms provide SSL certificates
3. **CORS**: Configure allowed origins for production
4. **Rate Limiting**: Consider adding rate limiting for API endpoints

---

## 🚨 **Troubleshooting**

### Common Issues

1. **Build Fails**
   - Check requirements.txt for missing dependencies
   - Verify Python version compatibility

2. **App Won't Start**
   - Check environment variables are set correctly
   - Verify Kafka credentials are valid

3. **Static Files Not Loading**
   - Ensure static folder is properly mounted
   - Check file paths in HTML

4. **Kafka Connection Issues**
   - Verify Confluent Cloud credentials
   - Check network connectivity
   - Ensure topic exists

### Debug Commands
```bash
# Check if app is running
curl https://your-app-url/health

# Test mood analysis
curl -X POST https://your-app-url/mood \
  -H "Content-Type: application/json" \
  -d '{"text": "I am happy!"}'
```

---

## 🎉 **Success!**

Once deployed, your AI DJ Streamer will be available at:
- **Render**: `https://your-app-name.onrender.com`
- **Railway**: `https://your-app-name.railway.app`
- **Heroku**: `https://your-app-name.herokuapp.com`

### Next Steps
1. Test all features work correctly
2. Set up monitoring and alerts
3. Configure custom domain (optional)
4. Share your live app! 🎵

---

**Need help?** Check the platform-specific documentation or open an issue on GitHub! 