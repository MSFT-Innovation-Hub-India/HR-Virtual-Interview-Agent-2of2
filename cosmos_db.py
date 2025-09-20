import os
import streamlit as st
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from typing import List, Dict, Any, Optional
from config import COSMOS_DB_CONFIG

class CosmosDBConnection:
    """
    Handles connection and operations with Azure Cosmos DB using DefaultAzureCredential
    """
    
    def __init__(self, endpoint: str, database_name: str, container_name: str):
        self.endpoint = endpoint
        self.database_name = database_name
        self.container_name = container_name
        self._client = None
        self._database = None
        self._container = None
    
    @st.cache_resource
    def _get_client(_self):
        """Initialize Cosmos DB client with DefaultAzureCredential"""
        try:
            credential = DefaultAzureCredential()
            return CosmosClient(url=_self.endpoint, credential=credential)
        except Exception as e:
            st.error(f"Failed to initialize Cosmos DB client: {str(e)}")
            return None
    
    def _get_container(self):
        """Get the container instance"""
        if not self._container:
            client = self._get_client()
            if client:
                self._database = client.get_database_client(self.database_name)
                self._container = self._database.get_container_client(self.container_name)
        return self._container
    
    @st.cache_data
    def get_all_interviews(_self) -> List[Dict[str, Any]]:
        """
        Retrieve all interview documents from the container
        """
        container = _self._get_container()
        if not container:
            return []
        
        try:
            # Query to get all documents
            query = "SELECT * FROM c"
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except Exception as e:
            st.error(f"Failed to retrieve interviews: {str(e)}")
            return []
    
    @st.cache_data
    def get_interview_by_id(_self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific interview document by ID
        """
        container = _self._get_container()
        if not container:
            return None
        
        try:
            # Query for specific document
            query = f"SELECT * FROM c WHERE c.id = @id"
            parameters = [{"name": "@id", "value": document_id}]
            
            items = list(container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            return items[0] if items else None
        except Exception as e:
            st.error(f"Failed to retrieve interview {document_id}: {str(e)}")
            return None
    
    @st.cache_data
    def get_interview_summary(_self) -> List[Dict[str, str]]:
        """
        Get a summary view of all interviews (candidate_name, position_applied, id)
        """
        container = _self._get_container()
        if not container:
            return []
        
        try:
            # Query to get all documents, then extract the fields we need
            query = "SELECT * FROM c"
            
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            # Transform the data for easier display
            summary = []
            for item in items:
                # Extract candidate info
                candidate_profile = item.get("candidate_profile", {})
                interview_feedback = item.get("interview_feedback", {})
                role_suitability = interview_feedback.get("role_suitability", {})
                
                # Format interview date for display
                interview_date = item.get("interview_date", "N/A")
                if interview_date and interview_date != "N/A":
                    try:
                        # Parse and format the date for better display
                        from datetime import datetime
                        if isinstance(interview_date, str):
                            date_obj = datetime.fromisoformat(interview_date.replace('Z', '+00:00'))
                            interview_date = date_obj.strftime("%Y-%m-%d")
                    except:
                        # If parsing fails, keep the original value
                        pass
                
                summary.append({
                    "id": item.get("id", "Unknown"),
                    "interview_date": interview_date,
                    "candidate_name": candidate_profile.get("candidate_name", "N/A"),
                    "position_applied": candidate_profile.get("position_applied", "N/A"),
                    "verdict": role_suitability.get("verdict", "N/A")
                })
            
            return summary
        except Exception as e:
            st.error(f"Failed to retrieve interview summary: {str(e)}")
            # Let's also print the actual error for debugging
            st.error(f"Debug info: {e}")
            return []

# Global connection instance
@st.cache_resource
def get_cosmos_connection():
    return CosmosDBConnection(
        COSMOS_DB_CONFIG["endpoint"], 
        COSMOS_DB_CONFIG["database_name"], 
        COSMOS_DB_CONFIG["container_name"]
    )