# Credit Card Validator API

A Django REST Framework API that validates credit card numbers using the Luhn algorithm and detects card schemes (Visa, Mastercard, American Express, Discover).

## Features

- ✅ **Luhn Algorithm Validation** - Industry-standard checksum validation
- ✅ **Card Scheme Detection** - Identifies Visa, Mastercard, Amex, Discover
- ✅ **Input Sanitization** - Automatically removes spaces and dashes
- ✅ **Comprehensive Error Handling** - Clear error messages for invalid inputs
- ✅ **Structured Logging** - Masked card numbers for security
- ✅ **OpenAPI Documentation** - Interactive Swagger UI
- ✅ **Full Test Coverage** - 36 unit tests covering all functionality

## Requirements

- Python 3.12+
- Django 5.1+
- Django REST Framework 3.14+
- drf-spectacular 0.27+

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/brianhuynh2021/lhv-credit-card-validator
cd lhv-credit-card-validator
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py migrate
```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Validate Credit Card Number

**Endpoint:** `POST /api/v1/validate/`

**Request Body:**
```json
{
  "number": "4532-0151-1283-0366"
}
```

**Success Response (200 OK):**
```json
{
  "valid": true,
  "scheme": "visa",
  "message": "OK"
}
```

**Invalid Card Response (200 OK):**
```json
{
  "valid": false,
  "scheme": "visa",
  "message": "Invalid card number"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Number must be between 12 and 19 digits."
}
```

#### Example Usage with cURL:
```bash
# Valid card
curl -X POST http://localhost:8000/api/v1/validate/ \
  -H "Content-Type: application/json" \
  -d '{"number": "4532015112830366"}'

# Card with spaces
curl -X POST http://localhost:8000/api/v1/validate/ \
  -H "Content-Type: application/json" \
  -d '{"number": "4532 0151 1283 0366"}'

# Invalid card
curl -X POST http://localhost:8000/api/v1/validate/ \
  -H "Content-Type: application/json" \
  -d '{"number": "4532015112830367"}'
```

### 2. Health Check

**Endpoint:** `GET /api/v1/health/`

**Response (200 OK):**
```json
{
  "status": "Ok"
}
```

#### Example Usage:
```bash
curl http://localhost:8000/api/v1/health/
```

## API Documentation

Interactive API documentation is available via Swagger UI:

- **Swagger UI:** http://localhost:8000/docs/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

## Supported Card Schemes

| Scheme          | Prefix Pattern | Example Number       | Length    |
|-----------------|----------------|----------------------|-----------|
| Visa            | 4              | 4532015112830366     | 13-19     |
| Mastercard      | 51-55          | 5425233430109903     | 16        |
| American Express| 34, 37         | 374245455400126      | 15        |
| Discover        | 6              | 6011000000000012     | 16-19     |
| Unknown         | Other          | -                    | 12-19     |

## Input Validation Rules

1. **Length:** Must be between 12 and 19 digits after sanitization
2. **Characters:** Only numeric digits allowed (spaces and dashes are automatically removed)
3. **Checksum:** Must pass Luhn algorithm validation

### Valid Input Formats:
- `4532015112830366` (plain)
- `4532 0151 1283 0366` (with spaces)
- `4532-0151-1283-0366` (with dashes)
- `4532-0151 1283-0366` (mixed)

## Running Tests

### Run all tests:
```bash
python manage.py test validator
```

### Run with verbose output:
```bash
python manage.py test validator --verbosity=2
```

### Run specific test class:
```bash
python manage.py test validator.tests.LuhnCheckTests
```

### Test Coverage:
The project includes 36 unit tests covering:
- ✅ Luhn algorithm validation (5 tests)
- ✅ Card scheme detection (7 tests)
- ✅ Input sanitization (4 tests)
- ✅ Length validation (4 tests)
- ✅ Digit validation (3 tests)
- ✅ Number masking (3 tests)
- ✅ API endpoints (9 tests)
- ✅ Health check (1 test)

## Logging

All validation requests are logged with the following information:
- **Scheme:** Detected card scheme
- **Valid:** Validation result (true/false)
- **Masked Number:** Only last 4 digits shown (e.g., `****0366`)
- **Request ID:** Unique identifier for request tracing

### Log Example:
```
INFO Card validation completed scheme=visa valid=True masked_number=****0366 request_id=abc123
```

## Project Structure

```
lhv-credit-card-validator/
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   ├── logging.py          # Logging configuration
│   ├── wsgi.py
│   └── asgi.py
├── validator/               # Main application
│   ├── __init__.py
│   ├── views.py            # API view classes
│   ├── serializers.py      # DRF serializers
│   ├── validators.py       # Validation logic (Luhn, schemes)
│   ├── tests.py            # Unit tests
│   ├── urls.py             # App URL routing
│   └── migrations/
├── manage.py
├── requirements.txt
└── README.md
```

## Security Considerations

- ✅ **No Data Storage:** Card numbers are never stored in database
- ✅ **Masked Logging:** Only last 4 digits visible in logs
- ✅ **Input Sanitization:** Prevents injection attacks
- ✅ **Validation:** Strict input validation rules
- ⚠️ **HTTPS Required:** Use HTTPS in production
- ⚠️ **CORS Configuration:** Configure allowed origins for production

## Troubleshooting

### Tests failing with 301 redirects
Ensure all test URLs have trailing slashes: `/api/v1/validate/` not `/api/v1/validate`

### Module not found errors
Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Port already in use
Change the port when running:
```bash
python manage.py runserver 8001
```

## Deployment Guide - Step by Step

### Prerequisites
- AWS Account with EC2 access
- SSH key pair (.pem file)
- Git repository with your code (GitHub, GitLab, or Bitbucket)

---

## Step 1: Launch EC2 Instance

### 1.1. Go to AWS Console
```
- Login to AWS Console (https://console.aws.amazon.com)
- Navigate to EC2 Dashboard
- Click "Launch Instance"
```

### 1.2. Configure Instance
```
Name: card-validator-api
Application and OS Images (AMI): Ubuntu Server 22.04 LTS (Free tier eligible)
Instance type: t2.micro (Free tier eligible)
Key pair: 
  - Create new key pair OR select existing
  - Name: card-validator-key
  - Type: RSA
  - Format: .pem
  - Download and save the .pem file securely
```

### 1.3. Configure Security Group
```
Create security group with these inbound rules:

Rule 1 - SSH:
  - Type: SSH
  - Protocol: TCP
  - Port: 22
  - Source: My IP (your current IP)
  
Rule 2 - Custom TCP (API):
  - Type: Custom TCP
  - Protocol: TCP
  - Port: 8000
  - Source: 0.0.0.0/0 (Anywhere)
  
Rule 3 - HTTP (Optional):
  - Type: HTTP
  - Protocol: TCP
  - Port: 80
  - Source: 0.0.0.0/0
```
**Outbound Rules:**
```
IMPORTANT: Allow outbound internet access for Docker to download images and apt packages

Rule 1 - All Traffic (Recommended):
  - Type: All traffic
  - Protocol: All
  - Port range: All
  - Destination: 0.0.0.0/0

OR minimum required:

Rule 1 - HTTP:
  - Type: HTTP
  - Protocol: TCP
  - Port: 80
  - Destination: 0.0.0.0/0
  
Rule 2 - HTTPS:
  - Type: HTTPS
  - Protocol: TCP
  - Port: 443
  - Destination: 0.0.0.0/0
```

### 1.4. Launch
```
- Review configuration
- Click "Launch Instance"
- Wait for instance state = "Running"
- Copy the Public IPv4 address (e.g., 3.84.137.206)
```

---

## Step 2: Connect to EC2 Instance

### 2.1. Set correct permissions for .pem file (First time only)
```bash
chmod 400 /path/to/card-validator-key.pem
```

### 2.2. SSH into EC2
```bash
ssh -i card-validator-key.pem ubuntu@3.84.137.206
```


**Expected output:**
```
Welcome to Ubuntu 22.04 LTS
...
ubuntu@ip-xxx-xxx-xxx-xxx:~$
```

---

## Step 3: Install Required Software on EC2

### 3.1. Update system packages

**Note:** If you encounter IPv6 connection errors (common on EC2), force IPv4:

```bash
# Update with IPv4 only (recommended)
sudo apt-get -o Acquire::ForceIPv4=true update
sudo apt-get -o Acquire::ForceIPv4=true upgrade -y

# Make permanent to avoid future issues
echo 'Acquire::ForceIPv4 "true";' | sudo tee /etc/apt/apt.conf.d/99force-ipv4
```

**Alternative:** If no IPv6 issues:
```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2. Install Docker
```bash
# Install Docker (will use IPv4 if configured above)
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

docker --version
sudo systemctl status docker

**Expected output:** `Docker version 24.x.x, build xxxxx`

### 3.3. Install Git
```bash
sudo apt install git -y

# Verify
git --version
```

### 3.4. Add ubuntu user to docker group
```bash
# Add user to docker group
sudo usermod -aG docker ubuntu

# Apply group changes (important!)
newgrp docker

# Verify - this should work without sudo
docker ps
```

---

## Step 4: Clone Project

### Option A: Clone from Git (Recommended)

```bash
# Clone your repository
git clone https://github.com/brianhuynh2021/lhv-credit-card-validator.git

# Navigate to project
cd lhv-credit-card-validator

# Verify files
ls -la
```

**Expected files:**
```
config/
validator/
Dockerfile
deploy-docker.sh
requirements.txt
README.md
manage.py
```


## Step 5: Configure Application [Optional] just for local

### 5.1. Update ALLOWED_HOSTS

```bash
# Edit settings file
nano config/settings.py
```

Find the line with `ALLOWED_HOSTS` and update:

```python
ALLOWED_HOSTS = ['3.84.137.206', 'localhost', '127.0.0.1']
```

Replace `3.84.137.206` with your actual EC2 Public IP.

**Save and exit:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 5.2. Verify Dockerfile

```bash
cat Dockerfile
```


---

## Step 6: Deploy with Docker

```bash
bash deploy-docker.sh
```
---

## Step 7: Verify Deployment

Open browser:
```
http://3.84.137.206:8000/docs/
```

You should see Swagger UI with API documentation.

---

## Author
Brian Huynh
LHV Bank - Credit Card Validator Take-Home Assignment

## Contributing

This is a take-home assignment project. For Testing only