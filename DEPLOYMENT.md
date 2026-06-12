# ResumeBoost AI - Deployment Guide

## Production Deployment Options

### Option 1: Docker Compose on Linux Server (Recommended for MVP)

**Prerequisites:**
- Ubuntu 20.04+ or similar Linux distro
- Docker & Docker Compose installed
- Domain name (optional but recommended)
- SSL certificate (Certbot/Let's Encrypt)

**Steps:**

1. **SSH into server:**
```bash
ssh user@your-server-ip
```

2. **Clone repository:**
```bash
git clone <your-repo-url> resumeboost
cd resumeboost
```

3. **Setup environment:**
```bash
cat > .env << EOF
OPENAI_API_KEY=your-openai-key
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
ENVIRONMENT=production
EOF
```

4. **Create production docker-compose:**
```bash
cp docker-compose.yml docker-compose.prod.yml
# Edit docker-compose.prod.yml for production settings
```

5. **Configure Nginx:**
```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx config
sudo tee /etc/nginx/sites-available/resumeboost << EOF
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location /api {
        proxy_pass http://backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/resumeboost /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

6. **Setup SSL with Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --standalone -d your-domain.com
```

7. **Start services:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: AWS Deployment (EC2 + RDS + S3)

**Architecture:**
```
User → CloudFront (CDN)
     ↓
  Route53 (DNS)
     ↓
  ELB (Load Balancer)
     ↓
  EC2 Auto Scaling Group
  ├── FastAPI Backend
  └── React Frontend
     ↓
  RDS PostgreSQL
  ↓
  S3 (Resume uploads)
```

**Steps:**

1. **Create EC2 instance:**
- Ubuntu 20.04 LTS AMI
- t3.medium instance (at least)
- 50GB EBS volume
- Security group allowing ports: 22, 80, 443, 8000

2. **Create RDS PostgreSQL:**
- PostgreSQL 13+
- db.t3.micro (minimum)
- Multi-AZ for production
- Backup retention: 7 days

3. **Create S3 bucket:**
- Enable versioning
- Set lifecycle policies
- Configure CORS

4. **SSH into EC2 and setup:**
```bash
# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose nginx -y

# Clone repository
git clone <your-repo> resumeboost
cd resumeboost

# Setup environment
cat > .env << EOF
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/resumeboost
OPENAI_API_KEY=your-key
S3_BUCKET=your-bucket
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
DEBUG=False
ENVIRONMENT=production
EOF

# Start services
docker-compose up -d
```

5. **Configure CloudFront:**
- Origin: ELB
- Cache behavior: 24 hours for static, 0 for API
- Compress objects
- HTTPS only

### Option 3: Kubernetes Deployment (Scalable)

**Prerequisites:**
- Kubernetes cluster (EKS, GKE, or self-managed)
- kubectl configured
- Helm (optional)

**Files structure:**
```
k8s/
├── namespace.yaml
├── configmap.yaml
├── secrets.yaml
├── backend-deployment.yaml
├── backend-service.yaml
├── frontend-deployment.yaml
├── frontend-service.yaml
├── postgres-statefulset.yaml
├── ingress.yaml
└── hpa.yaml (autoscaling)
```

**Example deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resumeboost-backend
  namespace: resumeboost
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/resumeboost-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-key
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Deploy to Kubernetes:**
```bash
# Create namespace
kubectl create namespace resumeboost

# Create secrets
kubectl create secret generic db-credentials \
  -n resumeboost \
  --from-literal=url=postgresql://...

kubectl create secret generic openai-key \
  -n resumeboost \
  --from-literal=api-key=sk-...

# Deploy
kubectl apply -f k8s/

# Check status
kubectl get pods -n resumeboost
kubectl logs -n resumeboost deployment/resumeboost-backend
```

## Production Environment Variables

### Backend Production (.env)

```env
# Environment
DEBUG=False
ENVIRONMENT=production

# Database (use PostgreSQL for production)
DATABASE_URL=postgresql://resumeboost_user:strong_password@db.example.com:5432/resumeboost_db
DATABASE_ECHO=False

# API
API_TITLE=ResumeBoost AI
API_VERSION=1.0.0
API_PREFIX=/api/v1

# JWT Security
SECRET_KEY=your-super-secret-key-32-chars-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-your-production-key
OPENAI_MODEL=gpt-4
OPENAI_BASE_URL=https://api.openai.com/v1

# File Upload (Use S3 in production)
MAX_FILE_SIZE=52428800  # 50MB
UPLOAD_DIR=/mnt/uploads

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
```

### Frontend Production (.env.production)

```env
VITE_API_URL=https://api.yourdomain.com/api/v1
VITE_APP_VERSION=1.0.0
```

## Database Migrations

### Using Alembic (Optional but Recommended)

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "initial_schema"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring & Logging

### Application Monitoring

**Using Prometheus + Grafana:**

```bash
# Install Prometheus
docker run -d \
  -p 9090:9090 \
  -v prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Install Grafana
docker run -d \
  -p 3001:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana
```

### Application Logging

**Using ELK Stack (Elasticsearch, Logstash, Kibana):**

```bash
# Add logging to FastAPI
from pythonjsonlogger import jsonlogger

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
})
```

## Backups & Disaster Recovery

### Database Backups

**PostgreSQL automated backup:**
```bash
# Create backup script
#!/bin/bash
BACKUP_DIR=/backups
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump resumeboost_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://your-backup-bucket/

# Cron job (daily at 2 AM)
0 2 * * * /usr/local/bin/backup_db.sh
```

### File Backups (S3)

```bash
# Enable S3 versioning
aws s3api put-bucket-versioning \
  --bucket your-upload-bucket \
  --versioning-configuration Status=Enabled

# Lifecycle policy
{
  "Rules": [
    {
      "Id": "DeleteOldVersions",
      "NoncurrentVersionExpirationInDays": 30,
      "Status": "Enabled"
    }
  ]
}
```

## Performance Optimization

### Backend Optimization

```python
# Enable response caching
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache2.init(RedisBackend(redis), prefix="fastapi-cache")

# Use @cache() decorator on endpoints
```

### Frontend Optimization

```bash
# Enable compression in Nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss;
gzip_min_length 1000;

# Enable caching headers
add_header Cache-Control "public, max-age=3600" always;
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (Security Groups)
- [ ] Enable database encryption
- [ ] Set up rate limiting
- [ ] Enable CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable audit logging
- [ ] Set up DDoS protection (Cloudflare/AWS Shield)
- [ ] Regular security updates
- [ ] Set up monitoring alerts
- [ ] Test disaster recovery

## Auto-Scaling Configuration

### AWS Auto Scaling Group

```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name resumeboost \
  --version-description "ResumeBoost Backend" \
  --launch-template-data '{
    "ImageId": "ami-0c55b159cbfafe1f0",
    "InstanceType": "t3.medium",
    "KeyName": "my-key",
    "SecurityGroupIds": ["sg-0123456789abcdef0"]
  }'

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name resumeboost-asg \
  --launch-template LaunchTemplateName=resumeboost \
  --min-size 2 \
  --max-size 6 \
  --desired-capacity 3 \
  --availability-zones us-east-1a us-east-1b us-east-1c
```

## Maintenance

### Database Maintenance

```bash
# Analyze and vacuum PostgreSQL
VACUUM ANALYZE;

# Check connections
SELECT * FROM pg_stat_activity;

# Monitor performance
SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC;
```

### Log Rotation

```bash
# Configure logrotate for application logs
cat > /etc/logrotate.d/resumeboost << EOF
/var/log/resumeboost/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
EOF
```

## Rollback Procedure

```bash
# Keep previous image tags
docker tag resumeboost-backend:latest resumeboost-backend:v1.0.0

# Rollback to previous version
docker-compose down
docker-compose -f docker-compose.prod.yml pull resumeboost-backend:v1.0.0
docker-compose -f docker-compose.prod.yml up -d
```

## Support & Troubleshooting

- Monitor logs: `docker-compose logs -f backend`
- Check service health: `curl https://yourdomain.com/health`
- Database connections: `psql -U user -d resumeboost_db`
- Nginx config test: `nginx -t`

---

**Production Ready Deployment! 🚀**
