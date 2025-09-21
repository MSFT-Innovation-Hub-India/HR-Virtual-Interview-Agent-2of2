# Configuration file for the Interview Outcome Viewer
import os

# Customer Branding Configuration
# Can be overridden by environment variables
CUSTOMER_CONFIG = {
    "company_name": os.getenv("COMPANY_NAME", "PhonePe"),
    "company_logo_url": os.getenv("COMPANY_LOGO_URL", ""),  # Optional logo URL
    "brand_color": os.getenv("BRAND_COLOR", "#5f259f"),  # PhonePe purple
    "secondary_color": os.getenv("SECONDARY_COLOR", "#ffffff"),
    "accent_color": os.getenv("ACCENT_COLOR", "#00d4aa"),  # PhonePe teal
    "app_title": os.getenv("APP_TITLE", "PhonePe HR Interview Outcomes"),
    "app_subtitle": os.getenv("APP_SUBTITLE", "Streamlined Candidate Assessment Dashboard"),
    "favicon": os.getenv("FAVICON", "📱"),  # PhonePe mobile app icon
}

# Azure Cosmos DB Configuration
# Can be overridden by environment variables
COSMOS_DB_CONFIG = {
    "endpoint": os.getenv("COSMOS_DB_ENDPOINT", "https://common-nosql-db.documents.azure.com:443/"),
    "database_name": os.getenv("COSMOS_DB_DATABASE", "db001"),
    "container_name": os.getenv("COSMOS_DB_CONTAINER", "hr-interview-assessment")
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": CUSTOMER_CONFIG["app_title"],
    "page_icon": CUSTOMER_CONFIG["favicon"],
    "layout": "wide"
}

# Display Configuration
DISPLAY_CONFIG = {
    "conversation_max_height": "600px",
    "max_records_per_page": 50,
    "search_placeholder": f"Search candidates for {CUSTOMER_CONFIG['company_name']} positions..."
}