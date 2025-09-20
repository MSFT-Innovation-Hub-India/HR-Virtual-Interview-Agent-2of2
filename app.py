import streamlit as st
import pandas as pd
from datetime import datetime
from cosmos_db import get_cosmos_connection
from typing import Dict, Any
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip loading .env file

# Configure page
st.set_page_config(
    page_title="HR Interview Outcome Viewer",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .candidate-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    
    .conversation-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-right: 2rem;
    }
    
    .role-label {
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .user-label {
        color: #1565c0;
    }
    
    .assistant-label {
        color: #7b1fa2;
    }
    
    .assessment-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    .verdict-go {
        background-color: #c8e6c9;
        color: #2e7d32;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
    }
    
    .verdict-no-go {
        background-color: #ffcdd2;
        color: #c62828;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def show_conversation(conversation_data):
    """Display conversation in a chat-like format"""
    st.markdown("### 💬 Interview Conversation")
    
    # Create a container with custom height
    container = st.container()
    
    with container:
        for i, msg in enumerate(conversation_data):
            role = msg.get("role", "")
            message = msg.get("message", "")
            
            if role == "user":
                # User message - right aligned
                st.markdown(f"""
                <div style="
                    background-color: #e3f2fd; 
                    padding: 0.8rem; 
                    border-radius: 10px; 
                    margin: 0.5rem 0; 
                    margin-left: 2rem;
                ">
                    <div style="font-weight: bold; font-size: 0.9rem; color: #1565c0; margin-bottom: 0.3rem;">
                        👤 Candidate
                    </div>
                    <div>{message}</div>
                </div>
                """, unsafe_allow_html=True)
                
            elif role == "assistant":
                # Assistant message - left aligned
                st.markdown(f"""
                <div style="
                    background-color: #f3e5f5; 
                    padding: 0.8rem; 
                    border-radius: 10px; 
                    margin: 0.5rem 0; 
                    margin-right: 2rem;
                ">
                    <div style="font-weight: bold; font-size: 0.9rem; color: #7b1fa2; margin-bottom: 0.3rem;">
                        🤖 AI Interviewer
                    </div>
                    <div>{message}</div>
                </div>
                """, unsafe_allow_html=True)

def show_candidate_profile(profile_data):
    """Display candidate profile information"""
    st.markdown("### 👤 Candidate Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {profile_data.get('candidate_name', 'N/A')}")
        st.markdown(f"**Position Applied:** {profile_data.get('position_applied', 'N/A')}")
        st.markdown(f"**Recording Consent:** {'✅ Yes' if profile_data.get('consent_recording') else '❌ No'}")
    
    with col2:
        st.markdown(f"**Current Role:** {profile_data.get('current_role_title', 'N/A')}")
        st.markdown(f"**Current Organization:** {profile_data.get('current_role_org', 'N/A')}")
        st.markdown(f"**Travel Acknowledgment:** {profile_data.get('hybrid_travel_ack', 'N/A')}")

def show_tech_probe(tech_data):
    """Display technical probe information"""
    st.markdown("### 🔧 Technical Assessment")
    
    st.markdown(f"**Topic:** {tech_data.get('tech_probe_topic', 'N/A')}")
    st.markdown(f"**Summary:** {tech_data.get('tech_probe_summary', 'N/A')}")
    st.markdown(f"**Follow-ups Used:** {tech_data.get('followups_used', 0)}")

def show_interview_feedback(feedback_data):
    """Display interview feedback and assessment"""
    st.markdown("### 📋 Interview Feedback")
    
    # Role Suitability
    role_suit = feedback_data.get('role_suitability', {})
    verdict = role_suit.get('verdict', 'N/A')
    
    verdict_class = "verdict-go" if verdict == "GO" else "verdict-no-go"
    st.markdown(f"""
    <div class="assessment-section">
        <h4>🎯 Role Suitability</h4>
        <p><strong>Verdict:</strong> <span class="{verdict_class}">{verdict}</span></p>
        <p><strong>Justification:</strong> {role_suit.get('justification', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Communication Skills
    comm_skills = feedback_data.get('communication_skills', {})
    st.markdown(f"""
    <div class="assessment-section">
        <h4>🗣️ Communication Skills</h4>
        <p><strong>Assessment:</strong> {comm_skills.get('assessment', 'N/A')}</p>
        <p><strong>Reasoning:</strong> {comm_skills.get('reasoning', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Technical Competence
    tech_comp = feedback_data.get('technical_competence', {})
    st.markdown(f"""
    <div class="assessment-section">
        <h4>⚙️ Technical Competence</h4>
        <p><strong>Assessment:</strong> {tech_comp.get('assessment', 'N/A')}</p>
        <p><strong>Reasoning:</strong> {tech_comp.get('reasoning', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

def show_interview_detail(interview_data):
    """Show detailed view of a single interview"""
    st.markdown('<h1 class="main-header">📄 Interview Details</h1>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Interview List", type="secondary"):
        st.session_state.selected_interview = None
        st.rerun()
    
    # Create two columns for main content and conversation
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Candidate Profile
        show_candidate_profile(interview_data.get('candidate_profile', {}))
        st.markdown("---")
        
        # Technical Probe
        show_tech_probe(interview_data.get('tech_probe', {}))
        st.markdown("---")
        
        # Interview Feedback
        show_interview_feedback(interview_data.get('interview_feedback', {}))
        
        # Document metadata
        st.markdown("### 📄 Document Info")
        st.markdown(f"**Document ID:** `{interview_data.get('id', 'N/A')}`")
        
        # Display interview date
        interview_date = interview_data.get('interview_date', 'N/A')
        if interview_date and interview_date != 'N/A':
            try:
                # Parse and format the date for better display
                from datetime import datetime
                if isinstance(interview_date, str):
                    date_obj = datetime.fromisoformat(interview_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%B %d, %Y')
                    st.markdown(f"**Interview Date:** {formatted_date}")
                else:
                    st.markdown(f"**Interview Date:** {interview_date}")
            except:
                st.markdown(f"**Interview Date:** {interview_date}")
        else:
            st.markdown(f"**Interview Date:** N/A")
        
        if '_ts' in interview_data:
            timestamp = datetime.fromtimestamp(interview_data['_ts'])
            st.markdown(f"**Last Modified:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        # Conversation
        conversation_data = interview_data.get('conversation', [])
        if conversation_data:
            show_conversation(conversation_data)
        else:
            st.warning("No conversation data available for this interview.")

def show_interview_grid():
    """Show the main grid view of interviews"""
    st.markdown('<h1 class="main-header">👥 HR Interview Outcomes</h1>', unsafe_allow_html=True)
    
    # Get connection and data
    cosmos_conn = get_cosmos_connection()
    
    with st.spinner("Loading interview data..."):
        interview_summary = cosmos_conn.get_interview_summary()
    
    if not interview_summary:
        st.error("No interview data found or unable to connect to the database.")
        st.info("Please ensure you have proper Azure authentication configured.")
        
        # Show current configuration for debugging
        from config import COSMOS_DB_CONFIG
        with st.expander("🔧 Current Configuration"):
            st.json({
                "endpoint": COSMOS_DB_CONFIG["endpoint"],
                "database": COSMOS_DB_CONFIG["database_name"], 
                "container": COSMOS_DB_CONFIG["container_name"]
            })
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(interview_summary)
    
    # Debug: Show the actual data structure
    if st.checkbox("🔍 Debug: Show raw data"):
        st.json(interview_summary[:1] if interview_summary else [])  # Show first record
    
    # Show current configuration
    if st.checkbox("🔧 Show configuration"):
        from config import COSMOS_DB_CONFIG
        st.json({
            "endpoint": COSMOS_DB_CONFIG["endpoint"],
            "database": COSMOS_DB_CONFIG["database_name"], 
            "container": COSMOS_DB_CONFIG["container_name"]
        })
    
    # Overall metrics
    st.markdown("### 📈 Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Interviews", len(df))
    with col2:
        go_count = len(df[df['verdict'] == 'GO'])
        st.metric("GO Verdicts", go_count)
    with col3:
        no_go_count = len(df[df['verdict'] != 'GO'])
        st.metric("NO-GO Verdicts", no_go_count)
    with col4:
        if len(df) > 0:
            success_rate = (go_count / len(df)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Position-based statistics
    st.markdown("### 💼 Statistics by Position")
    if len(df) > 0:
        position_stats = df.groupby('position_applied').agg({
            'verdict': ['count', lambda x: (x == 'GO').sum()],
            'candidate_name': 'count'
        }).round(1)
        
        # Flatten the multi-level column names
        position_stats.columns = ['Total_Interviews', 'GO_Verdicts', 'Total_Count']
        position_stats['Success_Rate'] = (position_stats['GO_Verdicts'] / position_stats['Total_Interviews'] * 100).round(1)
        position_stats = position_stats.drop('Total_Count', axis=1)
        
        # Display position statistics in columns
        positions = position_stats.index.tolist()
        if positions:
            cols = st.columns(len(positions))
            for i, position in enumerate(positions):
                with cols[i]:
                    st.markdown(f"**{position}**")
                    st.write(f"📊 Total: {position_stats.loc[position, 'Total_Interviews']}")
                    st.write(f"✅ GO: {position_stats.loc[position, 'GO_Verdicts']}")
                    st.write(f"📈 Rate: {position_stats.loc[position, 'Success_Rate']}%")
    
    st.markdown("---")
    
    # Search and filter
    search_term = st.text_input("🔍 Search by candidate name or position:", "")
    
    if search_term:
        df_filtered = df[
            df['candidate_name'].str.contains(search_term, case=False, na=False) |
            df['position_applied'].str.contains(search_term, case=False, na=False)
        ]
    else:
        df_filtered = df
    
    # Display the data grouped by position
    st.markdown("### 📊 Interview Records (Grouped by Position)")
    
    if len(df_filtered) == 0:
        st.warning("No interviews match your search criteria.")
        return
    
    # Group by position and display
    grouped_df = df_filtered.groupby('position_applied')
    
    for position, group in grouped_df:
        # Position header with statistics
        go_count_pos = len(group[group['verdict'] == 'GO'])
        total_count_pos = len(group)
        success_rate_pos = (go_count_pos / total_count_pos * 100) if total_count_pos > 0 else 0
        
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4 style="margin: 0; color: #1f77b4;">💼 {position}</h4>
            <p style="margin: 0.5rem 0 0 0; color: #666;">
                {total_count_pos} interviews • {go_count_pos} GO verdicts • {success_rate_pos:.1f}% success rate
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Column headers for this group
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 1.5, 1.5, 1, 1])
        with col1:
            st.markdown("**👤 Candidate Name**")
        with col2:
            st.markdown("**💼 Position**")
        with col3:
            st.markdown("**📅 Interview Date**")
        with col4:
            st.markdown("**📋 Verdict**")
        with col5:
            st.markdown("**🆔 ID**")
        with col6:
            st.markdown("**⚡ Action**")
        
        # Display records for this position
        for idx, row in group.iterrows():
            verdict_icon = "✅" if row['verdict'] == 'GO' else "❌"
            
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 1.5, 1.5, 1, 1])
                
                with col1:
                    st.write(f"**{row['candidate_name']}**")
                with col2:
                    st.write(row['position_applied'])
                with col3:
                    st.write(row.get('interview_date', 'N/A'))
                with col4:
                    st.write(f"{verdict_icon} {row['verdict']}")
                with col5:
                    st.write(f"`{row['id'][:8]}...`")
                with col6:
                    if st.button("View", key=f"view_{row['id']}"):
                        st.session_state.selected_interview = row['id']
                        st.rerun()
        
        st.markdown("---")

def main():
    """Main application function"""
    # Initialize session state
    if 'selected_interview' not in st.session_state:
        st.session_state.selected_interview = None
    
    # Check if an interview is selected
    if st.session_state.selected_interview:
        # Show detailed view
        cosmos_conn = get_cosmos_connection()
        
        with st.spinner("Loading interview details..."):
            interview_data = cosmos_conn.get_interview_by_id(st.session_state.selected_interview)
        
        if interview_data:
            show_interview_detail(interview_data)
        else:
            st.error("Interview not found or unable to load.")
            st.session_state.selected_interview = None
            st.rerun()
    else:
        # Show grid view
        show_interview_grid()

if __name__ == "__main__":
    main()