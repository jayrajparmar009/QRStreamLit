import streamlit as st
import urllib.parse
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# Configure page
st.set_page_config(
    page_title="Selected AEs",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_selected_aes_from_url():
    """Extract selected AEs from URL query parameters"""
    try:
        # Get query parameters from the URL
        query_params = st.query_params
        selected_aes = query_params.get_all('ae') if 'ae' in query_params else []
        return selected_aes
    except:
        # Fallback to session state if URL parsing fails
        return st.session_state.get('selected_aes', [])

def get_rcm_data(ae_id):
    """Generate sample RCM data for an AE"""
    # Sample data structure
    data = {
        "AE-0001": [
            {"Risk": "Data Privacy Breach", "Control": "Encryption at Rest"},
            {"Risk": "Data Privacy Breach", "Control": "Access Control Matrix"},
            {"Risk": "Data Privacy Breach", "Control": "Regular Security Audits"},
            {"Risk": "System Downtime", "Control": "Redundant Infrastructure"},
            {"Risk": "System Downtime", "Control": "Automated Backup Systems"},
            {"Risk": "Regulatory Non-compliance", "Control": "Compliance Monitoring Dashboard"},
            {"Risk": "Regulatory Non-compliance", "Control": "Regular Training Programs"}
        ],
        "AE-0002": [
            {"Risk": "Financial Fraud", "Control": "Multi-level Approval Process"},
            {"Risk": "Financial Fraud", "Control": "Transaction Monitoring System"},
            {"Risk": "Financial Fraud", "Control": "Segregation of Duties"},
            {"Risk": "Operational Error", "Control": "Automated Error Detection"},
            {"Risk": "Operational Error", "Control": "Quality Assurance Reviews"},
            {"Risk": "Market Risk", "Control": "Portfolio Diversification"},
            {"Risk": "Market Risk", "Control": "Real-time Risk Monitoring"}
        ],
        "AE-0003": [
            {"Risk": "Cyber Security Attack", "Control": "Firewall Protection"},
            {"Risk": "Cyber Security Attack", "Control": "Intrusion Detection System"},
            {"Risk": "Cyber Security Attack", "Control": "Employee Security Training"},
            {"Risk": "Data Loss", "Control": "Regular Data Backups"},
            {"Risk": "Data Loss", "Control": "Data Recovery Procedures"},
            {"Risk": "Third Party Risk", "Control": "Vendor Risk Assessment"},
            {"Risk": "Third Party Risk", "Control": "Contract Management System"}
        ]
    }
    return data.get(ae_id, [])

def get_past_issues(ae_id):
    """Generate sample past issues for word cloud"""
    issues = {
        "AE-0001": [
            "security", "breach", "unauthorized", "access", "data", "privacy", "compliance", 
            "vulnerability", "incident", "malware", "phishing", "authentication", "encryption",
            "firewall", "monitoring", "audit", "risk", "control", "governance", "policy"
        ],
        "AE-0002": [
            "fraud", "transaction", "financial", "error", "reconciliation", "approval", 
            "authorization", "payment", "settlement", "accounting", "reporting", "variance",
            "investigation", "suspicious", "anomaly", "detection", "verification", "validation"
        ],
        "AE-0003": [
            "attack", "threat", "malicious", "virus", "ransomware", "exploit", "penetration",
            "hacking", "infiltration", "compromise", "weakness", "patch", "update", "defense",
            "protection", "isolation", "quarantine", "restoration", "recovery", "backup"
        ]
    }
    return issues.get(ae_id, [])

def get_related_events(ae_id):
    """Generate sample ORES (Operational Risk Event Summary) data"""
    events = {
        "AE-0001": [
            {"Event ID": "ORE-2024-001", "Date": "2024-12-15", "Description": "Unauthorized access attempt to customer database", "Severity": "High", "Status": "Resolved"},
            {"Event ID": "ORE-2024-002", "Date": "2024-11-28", "Description": "Data encryption failure in backup system", "Severity": "Medium", "Status": "Investigating"},
            {"Event ID": "ORE-2024-003", "Date": "2024-10-12", "Description": "Failed compliance audit finding", "Severity": "Medium", "Status": "Resolved"},
            {"Event ID": "ORE-2024-004", "Date": "2024-09-05", "Description": "Suspicious login activity detected", "Severity": "Low", "Status": "Monitoring"}
        ],
        "AE-0002": [
            {"Event ID": "ORE-2024-005", "Date": "2024-12-20", "Description": "Fraudulent transaction detected and blocked", "Severity": "High", "Status": "Resolved"},
            {"Event ID": "ORE-2024-006", "Date": "2024-11-15", "Description": "Payment processing error affecting multiple accounts", "Severity": "Medium", "Status": "Resolved"},
            {"Event ID": "ORE-2024-007", "Date": "2024-10-30", "Description": "Reconciliation discrepancy in monthly reports", "Severity": "Low", "Status": "Closed"},
            {"Event ID": "ORE-2024-008", "Date": "2024-09-18", "Description": "Unauthorized approval workflow bypass", "Severity": "Medium", "Status": "Investigating"}
        ],
        "AE-0003": [
            {"Event ID": "ORE-2024-009", "Date": "2024-12-10", "Description": "Malware detected in email attachment", "Severity": "High", "Status": "Contained"},
            {"Event ID": "ORE-2024-010", "Date": "2024-11-22", "Description": "DDoS attack on web services", "Severity": "High", "Status": "Mitigated"},
            {"Event ID": "ORE-2024-011", "Date": "2024-10-08", "Description": "Suspicious network traffic patterns", "Severity": "Medium", "Status": "Monitoring"},
            {"Event ID": "ORE-2024-012", "Date": "2024-08-25", "Description": "Failed security patch deployment", "Severity": "Low", "Status": "Resolved"}
        ]
    }
    return events.get(ae_id, [])

def main():
    # Title and header
    st.title("📋 Selected AE Details")
    st.markdown("---")
    
    # Get selected AEs from URL or session state
    selected_aes = get_selected_aes_from_url()
    
    # Also check session state (for when navigating via sidebar)
    if not selected_aes and 'selected_aes' in st.session_state:
        selected_aes = st.session_state.selected_aes
    
    if selected_aes:
        st.markdown("### 🎯 You have selected the following AE IDs:")
        for i, ae in enumerate(selected_aes, 1):
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**{i}.**")
                with col2:
                    st.markdown(f"**{ae}**")
                    st.caption(f"Details for {ae} - Status: Active")
        st.markdown("---")
        st.success(f"✅ Total AEs selected: **{len(selected_aes)}**")

        # --- OBJECTIVE / SUMMARY CARD ---
        st.markdown("#### Objective / Summary")
        st.markdown(
            """
            <div style='
                background-color: var(--secondary-background-color); 
                border: 1px solid var(--border-color); 
                border-radius: 10px; 
                padding: 24px; 
                margin-bottom: 24px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                color: var(--text-color);
            '>
            <b>Lorem Ipsum</b> dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Pellentesque euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien. Etiam euismod, urna eu tincidunt consectetur, nisi nisl aliquam enim, nec dictum nisi nisl eget sapien.
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- RCM TABLE ---
        st.markdown("#### RCM Table")
        for ae in selected_aes:
            st.markdown(f"**RCM for {ae}:**")
            rcm_data = get_rcm_data(ae)
            if rcm_data:
                df = pd.DataFrame(rcm_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No RCM data available.")

        # --- PAST ISSUE WORD CLOUD ---
        st.markdown("#### Past Issues (Word Cloud)")
        for ae in selected_aes:
            st.markdown(f"**Past Issues for {ae}:**")
            issues = get_past_issues(ae)
            if issues:
                text = " ".join(issues * 10)  # repeat for better word cloud
                wc = WordCloud(width=600, height=300, background_color='white').generate(text)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("No past issues found.")

        # --- RELATED EVENTS TABLE ---
        st.markdown("#### Related Events (ORES)")
        for ae in selected_aes:
            st.markdown(f"**Related Events for {ae}:**")
            events = get_related_events(ae)
            if events:
                df = pd.DataFrame(events)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No related events found.")

        # --- Action Buttons ---
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔙 Back to Selection", use_container_width=True):
                st.switch_page("Home.py")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation feature coming soon!")
        with col3:
            if st.button("📤 Export Data", use_container_width=True):
                export_data = "\n".join([f"- {ae}" for ae in selected_aes])
                st.download_button(
                    label="Download as TXT",
                    data=export_data,
                    file_name="selected_aes.txt",
                    mime="text/plain"
                )
    else:
        st.warning("⚠️ No AE IDs were found!")
        st.markdown("This might happen if:")
        st.markdown("- You navigated directly to this page without scanning a QR code")
        st.markdown("- The QR code data was not properly transmitted")
        st.markdown("- The URL parameters were cleared")
        st.markdown("---")
        if st.button("🔙 Go to AE Selection Page", use_container_width=True):
            st.switch_page("Home.py")

if __name__ == "__main__":
    main()
