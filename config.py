# Configuration file for the Interview Outcome Viewer
import os

# Azure Cosmos DB Configuration
# Can be overridden by environment variables
COSMOS_DB_CONFIG = {
    "endpoint": os.getenv("COSMOS_DB_ENDPOINT", "https://common-nosql-db.documents.azure.com:443/"),
    "database_name": os.getenv("COSMOS_DB_DATABASE", "db001"),
    "container_name": os.getenv("COSMOS_DB_CONTAINER", "hr-interview-assessment")
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "HR Interview Outcome Viewer",
    "page_icon": "👥",
    "layout": "wide"
}

# Display Configuration
DISPLAY_CONFIG = {
    "conversation_max_height": "600px",
    "max_records_per_page": 50,
    "search_placeholder": "Search by candidate name or position..."
}