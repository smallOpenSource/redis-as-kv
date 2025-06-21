# Sample Configuration Files

This folder contains sample connection information for various services that can be stored using `redis_keyvault.py`.

## Included Samples

### 1. OpenSearch (`opensearch.json`)
- Basic connection information (hostname, port, username, password)
- Index and SSL settings
- Cluster information

### 2. MariaDB (`mariadb.json`)
- Database connection information
- SSL settings
- Basic options

### 3. Kafka (`kafka.json`)
- Broker connection information
- SASL/SSL security settings
- Topic and group settings

### 4. ProxySQL (`sample-proxysql.json`)
- ProxySQL connection information
- External access information
- MariaDB proxy settings

## Usage

### 1. Modify Sample Files
Modify each JSON file to match your actual environment:

```bash
# Edit files
notepad opensearch.json
notepad mariadb.json
notepad kafka.json
notepad sample-proxysql.json
```

### 2. Store in Redis KeyVault
Store modified configurations in Redis:

```bash
# Store each service configuration
python redis_keyvault.py save samples/opensearch.json
python redis_keyvault.py save samples/mariadb.json
python redis_keyvault.py save samples/kafka.json
python redis_keyvault.py save samples/sample-proxysql.json
```

### 3. Retrieve Stored Configurations
Check stored configurations:

```bash
# Retrieve each service configuration
python redis_keyvault.py get opensearch
python redis_keyvault.py get mariadb
python redis_keyvault.py get kafka
python redis_keyvault.py get sample-proxysql
```

## Important Notes

- **Do Not Use Sample Passwords**: Passwords in sample files are for demonstration only. Always change to actual authentication information in production environments.
- **Update Network Settings**: Modify hostnames and ports to match your actual service environment.
- **Security Settings**: Apply appropriate security settings in production environments.

## Additional Samples

If you need configuration samples for other services, you can create them using similar structures based on existing samples.
