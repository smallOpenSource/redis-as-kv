# Redis KeyVault v1.0.0 🚀

**Initial release of Redis KeyVault - A secure, encrypted key-value store using Redis Sentinel.**

## ✨ What's New
- 🔐 **Encrypted Storage**: Fernet encryption for all data and connection info
- 🏗️ **Redis Sentinel**: High availability cluster support (requires 3+ nodes)
- 💻 **CLI Tool**: `redis-keyvault` command for easy data management
- 🐍 **Python Library**: Import and use in your applications
- 📄 **JSON Support**: Store complex configurations securely
- 🌍 **Multi-language**: English and Korean documentation

## 📦 Installation
```bash
pip install redis_keyvault-1.0.0-py3-none-any.whl
```

## 🚀 Quick Start
```bash
# Setup (first run)
redis-keyvault

# Save config
redis-keyvault save myconfig.json

# Get config  
redis-keyvault get myconfig
```

## 📋 Requirements
- Python 3.6+
- Redis Sentinel cluster (3+ nodes)
- NOT compatible with standalone Redis

## 📁 Includes
- Core library with CLI
- Sample apps (OpenSearch, MariaDB, Kafka)
- Configuration templates
- Comprehensive docs (EN/KO)

## 🔒 Security
- Double encryption (data + connection)
- Encrypted .env storage
- Key namespacing

Perfect for storing database credentials, API keys, and service configurations securely! 🛡️
