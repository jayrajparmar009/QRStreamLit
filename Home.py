import streamlit as st
import qrcode
from io import BytesIO
import base64
from PIL import Image
import urllib.parse

# Configure page
st.set_page_config(
    page_title="AE Selection Portal",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def generate_qr_code(selected_aes):
    """Generate QR code for the selected AEs"""
    # Get the current app URL dynamically
    import os
    
    # Check if we're running on Streamlit Cloud or locally
    if 'STREAMLIT_SHARING_MODE' in os.environ or 'STREAMLIT_CLOUD' in os.environ:
        # Running on Streamlit Cloud - get the URL from the browser
        base_url = st.experimental_get_query_params().get('_url', [''])[0]
        if base_url:
            base_url = base_url.replace('/Home', '/Page_2')
        else:
            # Fallback for cloud deployment
            base_url = "https://your-app-name.streamlit.app/Page_2"
    else:
        # Running locally - use localhost
        base_url = "http://localhost:8501/Page_2"
    
    # Create the URL for page 2 with selected AEs as query parameters
    ae_params = "&".join([f"ae={ae}" for ae in selected_aes])
    full_url = f"{base_url}?{ae_params}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(full_url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for display
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def main():
    # Title and header
    st.title("🔍 AE Selection Portal")
    st.markdown("---")
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Select AE IDs")
        
        # AE IDs list
        ae_options = ["AE-0001", "AE-0002", "AE-0003"]
        
        # Multiselect widget
        selected_aes = st.multiselect(
            "Choose one or more AE IDs:",
            options=ae_options,
            placeholder="Select AE IDs...",
            help="Select at least one AE ID to generate a QR code"
        )
        
        # Display QR code if AEs are selected
        if selected_aes:
            st.markdown("---")
            st.markdown("### 📱 QR Code")
            st.markdown("Scan this QR code to view the selected AEs:")
            
            try:
                # Generate QR code
                qr_buffer = generate_qr_code(selected_aes)
                
                # Display QR code
                st.image(qr_buffer, width=300, caption="Scan to view selected AEs")
                
                # Show selected AEs for confirmation
                st.success(f"Selected AEs: {', '.join(selected_aes)}")
                
                # Additional info
                st.info("💡 Scan the QR code with your phone to navigate to the AE details page!")
                
            except Exception as e:
                st.error(f"Error generating QR code: {str(e)}")
        else:
            st.info("👆 Please select at least one AE ID to generate a QR code")

if __name__ == "__main__":
    main()
