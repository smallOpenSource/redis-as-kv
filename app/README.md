# Application Examples

This folder contains examples of using stored configurations from Redis KeyVault in real applications.

## Included Examples

### 1. OpenSearch Connection Example (`sample-opensearch.py`)
- Create OpenSearch client by loading opensearch configuration from Redis KeyVault
- Cluster information retrieval and connection testing
- Document indexing and searching examples

**Required packages:**
```bash
pip install opensearch-py
```

### 2. MariaDB Connection Example (`sample-mariadb.py`)
- Database connection by loading mariadb configuration from Redis KeyVault
- Connection status check and server information retrieval
- Table creation, data insertion/retrieval examples

**Required packages:**
```bash
pip install mysql-connector-python
```

### 3. Kafka Connection Example (`sample-kafka.py`)
- Producer/Consumer creation by loading kafka configuration from Redis KeyVault
- Connection testing and message sending/receiving examples
- SSL/SASL authentication support

**Required packages:**
```bash
pip install kafka-python
```

## Usage

### 1. Save Configurations
First, you need to save configuration files to Redis KeyVault:

```bash
# Modify configuration files to match your actual environment, then
python redis_keyvault.py save samples/opensearch.json
python redis_keyvault.py save samples/mariadb.json
python redis_keyvault.py save samples/kafka.json
```

### 2. Run Examples

Execute examples for each service:

```bash
# Run OpenSearch example
python app/sample-opensearch.py

# Run MariaDB example
python app/sample-mariadb.py

# Run Kafka example
python app/sample-kafka.py
```

## Features by Example

### OpenSearch Example
- **Connection Testing**: Check cluster information and status
- **Document Indexing**: Store sample log documents to index
- **Document Search**: Search and retrieve stored documents

### MariaDB Example
- **Connection Testing**: Check server version and database information
- **Table Operations**: Create sample table and insert data
- **Data Retrieval**: Query stored data and check table information
- **Cleanup Feature**: Option to clean up demo data

### Kafka Example
- **Connection Testing**: Connect to broker and send test messages
- **Producer**: Send various types of sample messages
- **Consumer**: Receive and process messages example
- **SSL/SASL**: Support for secure connections

## Prerequisites

1. **Package Installation**: Install required packages before running each example.
2. **Configuration Check**: Verify that correct configurations are stored in Redis KeyVault.
3. **Service Status**: Ensure that each service (OpenSearch, MariaDB, Kafka) is running.
4. **Network**: Check firewall and network connectivity.
5. **Permissions**: Verify you have appropriate access permissions for each service.

## Troubleshooting

### Common Issues
- `ModuleNotFoundError`: Install required packages
- Configuration not found: Check if configurations are stored in Redis KeyVault
- Connection failure: Verify service status and network connectivity

### Service-specific Issues
- **OpenSearch**: Check `verify_certs=False` setting for SSL certificate issues
- **MariaDB**: Verify database permissions and firewall settings
- **Kafka**: Check topic existence and security settings
