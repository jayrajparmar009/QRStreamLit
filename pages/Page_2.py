import streamlit as st
import urllib.parse

# Configure page
st.set_page_config(
    page_title="Selected AEs",
    page_icon="📋",
    layout="centered",
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
        
        # Display selected AEs in a nice format
        for i, ae in enumerate(selected_aes, 1):
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"**{i}.**")
                with col2:
                    st.markdown(f"**{ae}**")
                    # You can add more details about each AE here
                    st.caption(f"Details for {ae} - Status: Active")
        
        st.markdown("---")
        
        # Summary information
        st.success(f"✅ Total AEs selected: **{len(selected_aes)}**")
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔙 Back to Selection", use_container_width=True):
                # Clear query params and go back
                st.switch_page("Home.py")
        
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation feature coming soon!")
        
        with col3:
            if st.button("📤 Export Data", use_container_width=True):
                # Create a simple export
                export_data = "\\n".join([f"- {ae}" for ae in selected_aes])
                st.download_button(
                    label="Download as TXT",
                    data=export_data,
                    file_name="selected_aes.txt",
                    mime="text/plain"
                )
        
        # Additional information section
        st.markdown("---")
        st.markdown("### 📝 Additional Information")
        
        with st.expander("View AE Details"):
            for ae in selected_aes:
                st.markdown(f"**{ae}:**")
                st.markdown(f"- Type: Adverse Event")
                st.markdown(f"- Category: Medical")
                st.markdown(f"- Priority: Standard")
                st.markdown("")
    
    else:
        # No AEs selected
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
