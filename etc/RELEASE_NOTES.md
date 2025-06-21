# Redis KeyVault v1.0.0 Release

## 🎉 Initial Release

Redis KeyVault is a Python library that implements an encrypted key-value store using Redis Sentinel. This initial release provides secure storage and retrieval of sensitive information with enterprise-grade encryption.

## 🚀 Key Features

- **🔐 Encrypted Data Storage**: Secure data using Fernet encryption
- **🏗️ Redis Sentinel Support**: High availability through Redis Sentinel cluster connections
- **📄 JSON Data Support**: Store and retrieve complex data in JSON format
- **🔒 Environment Variable Encryption**: Redis connection information is also encrypted
- **💻 CLI Interface**: Easy command-line data storage and retrieval
- **🐍 Python Module**: Use as a library in your Python applications

## 📦 Installation

### From PyPI (when available)
```bash
pip install redis-keyvault
```

### From Release
```bash
pip install redis_keyvault-1.0.0-py3-none-any.whl
```

## 🔧 Quick Start

### CLI Usage
```bash
# Configure Redis Sentinel (first run)
redis-keyvault

# Save configuration
redis-keyvault save config.json

# Retrieve configuration
redis-keyvault get myconfig
```

### Python Module Usage
```python
from redis_keyvault import save_info, get_info

# Store data
data = {"host": "db.example.com", "port": 3306}
save_info("my-database", data)

# Retrieve data
config = get_info("my-database")
```

## 📋 Requirements

- **Python 3.6+**
- **Redis Sentinel Cluster** (minimum 3 nodes)
- Dependencies: `redis>=4.0.0`, `cryptography>=3.4.0`, `python-dotenv>=0.19.0`

> ⚠️ **Important**: This library requires Redis Sentinel cluster configuration and cannot be used with standalone Redis servers.

## 📁 What's Included

- **Core Library**: Encrypted key-value storage with Redis Sentinel
- **Sample Applications**: Real-world examples for OpenSearch, MariaDB, and Kafka
- **Sample Configurations**: Ready-to-use JSON configuration templates
- **Comprehensive Documentation**: English and Korean documentation

## 🔒 Security Features

- **Double Encryption**: Both data and Redis connection information are encrypted
- **Fernet Encryption**: Industry-standard symmetric encryption
- **Key Namespacing**: Organized storage with `info:` prefix
- **Environment Protection**: Encrypted `.env` file storage

## 📚 Documentation

- [English Documentation](README.md)
- [Korean Documentation](README-ko.md)
- [Application Examples](app/README.md)
- [Sample Configurations](samples/README.md)
- [Deployment Guide](DEPLOYMENT.md)

## 🧪 Examples Included

### Sample Applications (`app/` folder)
- **OpenSearch**: Document indexing and search operations
- **MariaDB**: Database connections and CRUD operations  
- **Kafka**: Producer/Consumer message processing

### Sample Configurations (`samples/` folder)
- OpenSearch cluster configuration
- MariaDB database settings
- Kafka broker setup
- ProxySQL configuration

## 🐛 Known Issues

- None reported for this initial release

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](README.md#contributing) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](README.md)
- 🐛 [Issue Tracker](../../issues)
- 💬 [Discussions](../../discussions)

## 🙏 Acknowledgments

Thank you to all contributors and the Redis community for making this project possible.

---

**Download the wheel file below to get started with Redis KeyVault!**
