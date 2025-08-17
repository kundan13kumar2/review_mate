# AI PR Reviewer 🤖

An intelligent GitHub App that automatically reviews pull requests using AI, providing code quality feedback and suggestions.

## 🚀 Features

- **Automated Code Review**: Automatically reviews PRs when they're opened, updated, or reopened
- **AI-Powered Analysis**: Uses OpenAI's GPT models to analyze code changes
- **Multi-Language Support**: Currently supports Java (easily extensible for other languages)
- **Smart File Filtering**: Focuses on modified files, skips removed files
- **Configurable Limits**: Adjustable file count and patch size limits for optimal performance
- **GitHub Integration**: Seamless integration via GitHub App and webhooks

## 🏗️ Architecture

- **FastAPI Backend**: Modern, fast web framework for handling GitHub webhooks
- **GitHub App**: Authenticated integration with GitHub repositories
- **OpenAI Integration**: AI-powered code analysis and review generation
- **Async Processing**: Non-blocking webhook handling for better performance

## 📋 Prerequisites

- Python 3.8+
- GitHub App credentials
- OpenAI API key
- ngrok (for local development)
- Docker (optional)

## 🚀 Quick Start with ngrok

### 1. Install ngrok
```bash
# Download from https://ngrok.com/download
# Or install via package manager
npm install -g ngrok  # Node.js
# or
brew install ngrok     # macOS
```

### 2. Clone and setup the project
```bash
git clone https://github.com/kundan13kumar2/review_mate.git
cd review_mate
pip install -r requirements.txt
```

### 3. Start your FastAPI app
```bash
python -m app.main
```
Your app will run on `http://localhost:3000`

### 4. Start ngrok tunnel
```bash
ngrok http 3000
```

You'll see output like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:3000
```

### 5. Configure GitHub App webhook
Use the ngrok URL as your webhook endpoint:
```
https://abc123.ngrok.io/api/webhook
```

## ⚙️ Installation & Setup

### Environment Configuration
Create a `.env` file:

```env
# GitHub App Configuration
GITHUB_APP_ID=your_github_app_id
GITHUB_INSTALLATION_ID=your_installation_id
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_PRIVATE_KEY_BASE64=your_base64_encoded_private_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Application Settings
PORT=3000
REVIEW_MAX_FILES=30
REVIEW_MAX_PATCH_CHARS=60000
```

### GitHub App Setup

1. **Create GitHub App**:
   - Go to [GitHub Developer Settings](https://github.com/settings/apps)
   - Click "New GitHub App"
   - Set App name: `AI PR Reviewer`
   - Set Homepage URL: `https://github.com/kundan13kumar2/review_mate`
   - Set Webhook URL: `https://your-ngrok-url.ngrok.io/api/webhook`
   - Set Webhook secret: Generate a secure random string

2. **Set Permissions**:
   - Repository permissions: `Contents: Read`
   - Pull request permissions: `Read`

3. **Install the App**:
   - Install in your repositories
   - Note the Installation ID

4. **Generate Private Key**:
   - Download the private key
   - Convert to base64: `base64 -i private-key.pem`

## 🧪 Testing with ngrok

### 1. Start your application
```bash
python -m app.main
```

### 2. Start ngrok tunnel
```bash
ngrok http 3000
```

### 3. Test webhook endpoint
```bash
curl -X GET https://your-ngrok-url.ngrok.io/api/first
# Should return: {"message":"Hello"}
```

### 4. Create a test PR
- Make changes in your repository
- Create a pull request
- Check your app logs for webhook events
- Verify AI review is generated

## 📁 Project Structure

```
ai_pr_reviewer/
├── app/
│   ├── __init__.py
│   ├── ai_client.py          # OpenAI integration
│   ├── config.py             # Configuration management
│   ├── deps.py               # Dependencies and middleware
│   ├── github_client.py      # GitHub API client
│   ├── gitToken.py           # GitHub authentication
│   ├── main.py               # FastAPI application
│   ├── review_service.py     # Core review logic
│   └── webhook.py            # GitHub webhook handlers
├── tests/
│   └── test_signature.py     # Test files
├── docker-compose.yml        # Docker configuration
├── Dockerfile                # Docker image
├── requirements.txt          # Python dependencies
└── test_run.py              # Test runner
```

## 🔍 How It Works

1. **Webhook Reception**: GitHub sends webhook events for PR actions
2. **Event Processing**: Filters for relevant PR events (opened, updated, reopened)
3. **File Analysis**: Retrieves changed files and their patches
4. **AI Review**: Sends code changes to OpenAI for analysis
5. **Review Creation**: Posts AI-generated reviews as PR comments
6. **Summary**: Provides overall PR summary with review statistics

## 🐳 Docker (Alternative to ngrok)

If you prefer Docker over ngrok:

```bash
# Build and run
docker-compose up --build

# Your app will be available at http://localhost:3000
# Use port forwarding or deploy to get a public URL
```

## 🧪 Testing

Run the test suite:
```bash
python test_run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common ngrok Issues

1. **Webhook not receiving events**:
   - Check ngrok is running: `ngrok http 3000`
   - Verify webhook URL in GitHub App settings
   - Check ngrok logs for incoming requests

2. **Authentication errors**:
   - Verify all environment variables are set
   - Check GitHub App permissions
   - Ensure private key is correctly base64 encoded

3. **Port already in use**:
   - Change port in `.env`: `PORT=3001`
   - Update ngrok: `ngrok http 3001`

### Debug Mode
Enable verbose logging by setting:
```env
LOG_LEVEL=DEBUG
```

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/kundan13kumar2/review_mate/issues) page
2. Create a new issue with:
   - Error logs
   - Environment details
   - ngrok URL (if using)
   - Steps to reproduce

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Integrated with [GitHub Apps](https://docs.github.com/en/apps)
- Local development with [ngrok](https://ngrok.com/)

---

**Note**: 
- Keep your API keys and GitHub credentials secure
- ngrok URLs change each time you restart (use ngrok pro for fixed URLs)
- Never commit `.env` files to version control
