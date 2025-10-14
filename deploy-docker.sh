#!/bin/bash
echo "🐳 Starting Docker deployment..."

# Pull latest code
git pull origin main

# Stop and remove old container (if exists)
docker stop card-validator 2>/dev/null || true
docker rm card-validator 2>/dev/null || true

# Remove old image (optional - để build fresh)
# docker rmi card-validator 2>/dev/null || true

# Build new image
echo "Building Docker image..."
docker build -t card-validator .

# Run new container
echo "Starting container..."
docker run -d \
  -p 8000:8000 \
  --name card-validator \
  --restart always \
  card-validator

echo "✅ Deployment complete!"
echo ""
echo "Container status:"
docker ps | grep card-validator

echo ""
echo "Recent logs:"
docker logs --tail 20 card-validator

echo ""
echo "🌐 Access API at: http://3.84.137.206:8000/api/v1/health/"