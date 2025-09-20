# Interview Outcome Viewer

A Streamlit web application to view and analyze HR virtual interview assessments stored in Azure Cosmos DB.

## Features

- Browse interview records in a scrollable grid
- View detailed interview outcomes and assessments
- Interactive conversation viewer with chat-like interface
- Azure authentication using default credentials

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Cosmos DB connection (choose one method):

   **Method A: Environment Variables**
   ```bash
   # Windows PowerShell
   $env:COSMOS_DB_ENDPOINT="https://your-cosmosdb-account.documents.azure.com:443/"
   $env:COSMOS_DB_DATABASE="your-database-name"
   $env:COSMOS_DB_CONTAINER="your-container-name"
   
   # Windows Command Prompt
   set COSMOS_DB_ENDPOINT=https://your-cosmosdb-account.documents.azure.com:443/
   set COSMOS_DB_DATABASE=your-database-name
   set COSMOS_DB_CONTAINER=your-container-name
   ```

   **Method B: .env File**
   ```bash
   # Copy the example file and edit it
   copy .env.example .env
   # Then edit .env with your actual values
   ```

   **Method C: Use Default Values**
   The app will use the default values from `config.py` if no environment variables are set.

3. Ensure Azure authentication is configured:
   - Use Azure CLI: `az login`
   - Or set up Azure identity (Managed Identity, Service Principal, etc.)

4. Run the application:
```bash
streamlit run app.py
```

## Configuration

### Default Configuration
The app connects to:
- Cosmos DB Endpoint: `https://common-nosql-db.documents.azure.com:443/`
- Database: `db001`
- Container: `hr-interview-assessment`

### Custom Configuration
You can override these values using environment variables:
- `COSMOS_DB_ENDPOINT` - Your Cosmos DB endpoint URL
- `COSMOS_DB_DATABASE` - Your database name  
- `COSMOS_DB_CONTAINER` - Your container name

### Environment Variables Priority
1. Environment variables (highest priority)
2. .env file values
3. Default values in config.py (lowest priority)

## Usage

1. The main page displays a grid of all interview records grouped by position
2. View overall and position-specific statistics
3. Click on any record to view detailed assessment
4. Use the conversation panel to review the interview dialogue