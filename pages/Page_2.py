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
    """Generate sample RCM data for an AE with Business Process and Test Steps"""
    data = {
        "AE-0001": [
            {
                "Risk": "Data Privacy Breach",
                "Control": "Encryption at Rest",
                "Business Process": "Data Management",
                "Test Steps": "1. Verify encryption method\n2. Check encryption logs\n3. Validate access restrictions"
            },
            {
                "Risk": "Data Privacy Breach",
                "Control": "Access Control Matrix",
                "Business Process": "User Access Management",
                "Test Steps": "1. Review user roles\n2. Validate access rights\n3. Confirm audit trail"
            },
            {
                "Risk": "Data Privacy Breach",
                "Control": "Regular Security Audits",
                "Business Process": "IT Security",
                "Test Steps": "1. Review past audit reports\n2. Verify follow-up actions\n3. Confirm audit frequency"
            },
            {
                "Risk": "System Downtime",
                "Control": "Redundant Infrastructure",
                "Business Process": "IT Operations",
                "Test Steps": "1. Inspect infrastructure setup\n2. Verify failover testing\n3. Check redundancy logs"
            },
            {
                "Risk": "System Downtime",
                "Control": "Automated Backup Systems",
                "Business Process": "Business Continuity",
                "Test Steps": "1. Test backup restoration\n2. Review backup logs\n3. Validate backup schedule"
            },
            {
                "Risk": "Regulatory Non-compliance",
                "Control": "Compliance Monitoring Dashboard",
                "Business Process": "Regulatory Compliance",
                "Test Steps": "1. Check dashboard settings\n2. Verify data accuracy\n3. Ensure timely updates"
            },
            {
                "Risk": "Regulatory Non-compliance",
                "Control": "Regular Training Programs",
                "Business Process": "HR & Compliance",
                "Test Steps": "1. Review training calendar\n2. Validate attendance logs\n3. Check content compliance"
            }
        ],
        "AE-0002": [
            {
                "Risk": "Financial Fraud",
                "Control": "Multi-level Approval Process",
                "Business Process": "Accounts Payable",
                "Test Steps": "1. Review approval hierarchy\n2. Sample transaction audit\n3. Validate segregation of duties"
            },
            {
                "Risk": "Financial Fraud",
                "Control": "Transaction Monitoring System",
                "Business Process": "Finance Control",
                "Test Steps": "1. Check monitoring rules\n2. Review flagged transactions\n3. Validate exception handling"
            },
            {
                "Risk": "Financial Fraud",
                "Control": "Segregation of Duties",
                "Business Process": "Financial Governance",
                "Test Steps": "1. Map roles and responsibilities\n2. Verify conflicting roles\n3. Review override logs"
            },
            {
                "Risk": "Operational Error",
                "Control": "Automated Error Detection",
                "Business Process": "Operations QA",
                "Test Steps": "1. Run error simulation\n2. Check detection alerts\n3. Review resolution workflow"
            },
            {
                "Risk": "Operational Error",
                "Control": "Quality Assurance Reviews",
                "Business Process": "Operational Risk",
                "Test Steps": "1. Check QA sampling process\n2. Review feedback reports\n3. Validate improvement actions"
            },
            {
                "Risk": "Market Risk",
                "Control": "Portfolio Diversification",
                "Business Process": "Investment Management",
                "Test Steps": "1. Analyze portfolio allocation\n2. Review diversification policy\n3. Validate exposure limits"
            },
            {
                "Risk": "Market Risk",
                "Control": "Real-time Risk Monitoring",
                "Business Process": "Market Surveillance",
                "Test Steps": "1. Review risk dashboards\n2. Check alert configurations\n3. Validate data feeds"
            }
        ],
        "AE-0003": [
            {
                "Risk": "Cyber Security Attack",
                "Control": "Firewall Protection",
                "Business Process": "Network Security",
                "Test Steps": "1. Review firewall rules\n2. Validate latest updates\n3. Check intrusion logs"
            },
            {
                "Risk": "Cyber Security Attack",
                "Control": "Intrusion Detection System",
                "Business Process": "IT Security",
                "Test Steps": "1. Test detection capabilities\n2. Review incident logs\n3. Confirm escalation protocols"
            },
            {
                "Risk": "Cyber Security Attack",
                "Control": "Employee Security Training",
                "Business Process": "HR Training",
                "Test Steps": "1. Review training frequency\n2. Validate test results\n3. Confirm participation"
            },
            {
                "Risk": "Data Loss",
                "Control": "Regular Data Backups",
                "Business Process": "Data Management",
                "Test Steps": "1. Check backup logs\n2. Validate storage health\n3. Review backup success rate"
            },
            {
                "Risk": "Data Loss",
                "Control": "Data Recovery Procedures",
                "Business Process": "Business Continuity",
                "Test Steps": "1. Test recovery process\n2. Review RTO and RPO\n3. Validate data integrity"
            },
            {
                "Risk": "Third Party Risk",
                "Control": "Vendor Risk Assessment",
                "Business Process": "Third Party Management",
                "Test Steps": "1. Review assessment reports\n2. Validate scoring criteria\n3. Confirm assessment frequency"
            },
            {
                "Risk": "Third Party Risk",
                "Control": "Contract Management System",
                "Business Process": "Vendor Governance",
                "Test Steps": "1. Check contract repository\n2. Validate expiry tracking\n3. Review approval workflows"
            }
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

def get_related_events(ae_id):
    """Generate extended ORES (Operational Risk Event Summary) data"""
    events = {
        "AE-0001": [
            {
                "Event ID": "ORE-2024-001",
                "Discover Date": "2024-12-15",
                "Summary": "Unauthorized DB access",
                "Description": "Unauthorized access attempt to customer database",
                "Gross Impact on Earnings": 100000,
                "CAD Equivalent": 135000,
                "GL Account Code": "610001",
                "GL Account Description": "Security Breach Expenses"
            },
            {
                "Event ID": "ORE-2024-002",
                "Discover Date": "2024-11-28",
                "Summary": "Encryption failure",
                "Description": "Data encryption failure in backup system",
                "Gross Impact on Earnings": 50000,
                "CAD Equivalent": 67500,
                "GL Account Code": "610002",
                "GL Account Description": "Data Protection Failures"
            }
        ],
        "AE-0002": [
            {
                "Event ID": "ORE-2024-005",
                "Discover Date": "2024-12-20",
                "Summary": "Fraud blocked",
                "Description": "Fraudulent transaction detected and blocked",
                "Gross Impact on Earnings": 250000,
                "CAD Equivalent": 337500,
                "GL Account Code": "620001",
                "GL Account Description": "Fraud Investigation Costs"
            },
            {
                "Event ID": "ORE-2024-006",
                "Discover Date": "2024-11-15",
                "Summary": "Payment error",
                "Description": "Payment processing error affecting multiple accounts",
                "Gross Impact on Earnings": 30000,
                "CAD Equivalent": 40500,
                "GL Account Code": "620002",
                "GL Account Description": "Payment Operation Errors"
            }
        ],
        "AE-0003": [
            {
                "Event ID": "ORE-2024-009",
                "Discover Date": "2024-12-10",
                "Summary": "Malware attack",
                "Description": "Malware detected in email attachment",
                "Gross Impact on Earnings": 150000,
                "CAD Equivalent": 202500,
                "GL Account Code": "630001",
                "GL Account Description": "Cybersecurity Breach Handling"
            },
            {
                "Event ID": "ORE-2024-010",
                "Discover Date": "2024-11-22",
                "Summary": "DDoS incident",
                "Description": "DDoS attack on web services",
                "Gross Impact on Earnings": 120000,
                "CAD Equivalent": 162000,
                "GL Account Code": "630002",
                "GL Account Description": "IT Infrastructure Incident Costs"
            }
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
        st.markdown("#### Recommended RCM Table")
        all_rcm_records = []

        for ae in selected_aes:
            rcm_data = get_rcm_data(ae)
            for record in rcm_data:
                record_with_ae = record.copy()
                record_with_ae["AE ID"] = ae  # add AE ID to identify the source
                all_rcm_records.append(record_with_ae)

        if all_rcm_records:
            merged_df = pd.DataFrame(all_rcm_records)
            st.dataframe(merged_df, use_container_width=True, hide_index=True)
        else:
            st.info("No RCM data available.")

        # --- PAST ISSUE WORD CLOUD ---
        # st.markdown("#### Past Issues (Word Cloud)")
        # for ae in selected_aes:
        #     st.markdown(f"**Past Issues for {ae}:**")
        #     issues = get_past_issues(ae)
        #     if issues:
        #         text = " ".join(issues * 10)  # repeat for better word cloud
        #         wc = WordCloud(width=600, height=300, background_color='white').generate(text)
        #         fig, ax = plt.subplots(figsize=(8, 4))
        #         ax.imshow(wc, interpolation='bilinear')
        #         ax.axis('off')
        #         st.pyplot(fig)
        #     else:
        #         st.info("No past issues found.")

        # --- RELATED EVENTS TABLE ---
        # st.markdown("#### Related Events (ORES)")
        # for ae in selected_aes:
        #     st.markdown(f"**Related Events for {ae}:**")
        #     events = get_related_events(ae)
        #     if events:
        #         df = pd.DataFrame(events)
        #         st.dataframe(df, use_container_width=True, hide_index=True)
        #     else:
        #         st.info("No related events found.")


        # with col3:
            # if st.button("📤 Export Data", use_container_width=True):
            #     export_data = "\n".join([f"- {ae}" for ae in selected_aes])
            #     st.download_button(
            #         label="Download as TXT",
            #         data=export_data,
            #         file_name="selected_aes.txt",
            #         mime="text/plain"
            #     )
        st.markdown("#### Related Events (ORES)")
        all_events = []

        for ae in selected_aes:
            events = get_related_events(ae)
            for event in events:
                event_with_ae = event.copy()
                event_with_ae["AE ID"] = ae
                all_events.append(event_with_ae)

        if all_events:
            events_df = pd.DataFrame(all_events)
            st.dataframe(events_df, use_container_width=True, hide_index=True)
        else:
            st.info("No related events found.")

        # --- PRIOR AUDITS TABLE ---
        st.markdown("#### Prior Audits")
        all_audits = []

        # Simulated inline audit data
        audit_data = {
            "AE-0001": [
                {"Audit ID": "AUD-2021-001", "Audit Title": "Data Privacy Controls", "Engagement Type": "Internal", "Audit Status": "Closed", "Audit Reporting Year": 2021},
                {"Audit ID": "AUD-2022-002", "Audit Title": "Cloud Security Review", "Engagement Type": "External", "Audit Status": "Closed", "Audit Reporting Year": 2022}
            ],
            "AE-0002": [
                {"Audit ID": "AUD-2020-003", "Audit Title": "Finance Compliance Audit", "Engagement Type": "Internal", "Audit Status": "Closed", "Audit Reporting Year": 2020},
                {"Audit ID": "AUD-2023-004", "Audit Title": "Payment Controls Review", "Engagement Type": "External", "Audit Status": "In Progress", "Audit Reporting Year": 2023}
            ],
            "AE-0003": [
                {"Audit ID": "AUD-2021-005", "Audit Title": "Cybersecurity Framework", "Engagement Type": "Internal", "Audit Status": "Closed", "Audit Reporting Year": 2021},
                {"Audit ID": "AUD-2022-006", "Audit Title": "Third Party Vendor Risk", "Engagement Type": "External", "Audit Status": "Closed", "Audit Reporting Year": 2022}
            ]
        }

        for ae in selected_aes:
            for audit in audit_data.get(ae, []):
                audit["AE ID"] = ae
                all_audits.append(audit)

        if all_audits:
            audit_df = pd.DataFrame(all_audits)
            st.dataframe(audit_df, use_container_width=True, hide_index=True)
        else:
            st.info("No prior audit records found.")

            # --- PRIOR ISSUES TABLE ---
        st.markdown("#### Prior Issues")
        all_issues = []

        # Simulated inline prior issue data
        issue_data = {
            "AE-0001": [
                {"Issue ID": "ISS-2021-001", "Issue Title": "Unencrypted backups found", "Issue Rating (1-5)": 4, "Audit Reporting Year": 2021},
                {"Issue ID": "ISS-2022-002", "Issue Title": "Access control gaps", "Issue Rating (1-5)": 3, "Audit Reporting Year": 2022}
            ],
            "AE-0002": [
                {"Issue ID": "ISS-2020-003", "Issue Title": "Transaction override logging missing", "Issue Rating (1-5)": 5, "Audit Reporting Year": 2020},
                {"Issue ID": "ISS-2023-004", "Issue Title": "Approval process inconsistent", "Issue Rating (1-5)": 2, "Audit Reporting Year": 2023}
            ],
            "AE-0003": [
                {"Issue ID": "ISS-2021-005", "Issue Title": "Outdated antivirus signatures", "Issue Rating (1-5)": 4, "Audit Reporting Year": 2021},
                {"Issue ID": "ISS-2022-006", "Issue Title": "Vendor risk documentation missing", "Issue Rating (1-5)": 3, "Audit Reporting Year": 2022}
            ]
        }

        for ae in selected_aes:
            for issue in issue_data.get(ae, []):
                issue["AE ID"] = ae
                all_issues.append(issue)

        if all_issues:
            issues_df = pd.DataFrame(all_issues)
            st.dataframe(issues_df, use_container_width=True, hide_index=True)
        else:
            st.info("No prior issues found.")
        # --- HISTORICAL DATA (CONSOLIDATED) ---
        st.markdown("#### 🗃️ Historical Data (Consolidated View)")

        # Gather all data types with a tag for type
        historical_data = []

        # Add RCM
        for ae in selected_aes:
            for row in get_rcm_data(ae):
                record = row.copy()
                record["AE ID"] = ae
                record["Source Type"] = "RCM"
                historical_data.append(record)

        # Add Related Events
        for ae in selected_aes:
            for row in get_related_events(ae):
                record = row.copy()
                record["AE ID"] = ae
                record["Source Type"] = "Related Event"
                historical_data.append(record)

        # Add Prior Audits
        for ae in selected_aes:
            for row in audit_data.get(ae, []):
                record = row.copy()
                record["AE ID"] = ae
                record["Source Type"] = "Prior Audit"
                historical_data.append(record)

        # # Add Prior Issues
        # for ae in selected_aes:
        #     for row in issue_data.get(ae, []):
        #         record = row.copy()
        #         record["AE ID"] = ae
        #         record["Source Type"] = "Prior Issue"
        #         historical_data.append(record)

        # Display 10 rows only
        if historical_data:
            hist_df = pd.DataFrame(historical_data)
            st.dataframe(hist_df.head(10), use_container_width=True, hide_index=True)

            # Excel export
            to_excel = io.BytesIO()
            # with pd.ExcelWriter(to_excel, engine='xlsxwriter') as writer:
            #     hist_df.to_excel(writer, index=False, sheet_name='Historical Data')
            # to_excel.seek(0)

            st.download_button(
                label="📥 Download Full Historical Data (Excel)",
                data=to_excel,
                file_name="historical_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No historical data available.")

        # --- Action Buttons ---
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔙 Back to Selection", use_container_width=True):
                st.switch_page("Home.py")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation feature coming soon!")

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
