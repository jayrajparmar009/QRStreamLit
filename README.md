# AE Selection Portal - Streamlit App

A multi-page Streamlit application for selecting AE IDs and generating QR codes for navigation.

## Features

- **Page 1 (Home)**: 
  - Multiselect widget with AE IDs: AE-0001, AE-0002, AE-0003
  - QR code generation when AEs are selected
  - Centered layout with clean UI

- **Page 2**: 
  - Displays selected AE IDs from QR code scan
  - Additional AE details and information
  - Export and report generation options

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run Home.py
   ```

   Or use the batch file (Windows):
   ```bash
   run_app.bat
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:8501`
   - The application will open on the Home page

## How to Use

### Page 1 - AE Selection
1. Select one or more AE IDs from the multiselect dropdown
2. A QR code will automatically generate once you select at least one AE
3. Scan the QR code with your mobile device or copy the URL

### Page 2 - AE Details
1. This page can be accessed by:
   - Scanning the QR code from Page 1
   - Using the sidebar navigation
   - Direct URL with parameters
2. View the selected AE IDs and their details
3. Use action buttons for export, reports, or navigation

## Project Structure

```
RCM/
├── Home.py                 # Main page with AE selection and QR code
├── pages/
│   └── Page_2.py          # AE details display page
├── requirements.txt       # Python dependencies
├── run_app.bat           # Windows batch file to run the app
└── README.md             # This file
```

## Dependencies

- `streamlit==1.29.0` - Web app framework
- `qrcode[pil]==7.4.2` - QR code generation
- `Pillow==10.1.0` - Image processing

## Technical Details

### QR Code Generation
- QR codes contain URLs that direct to Page 2 with selected AE IDs as query parameters
- Format: `http://localhost:8501/Page_2?ae=AE-0001&ae=AE-0002`

### Navigation
- Streamlit's native page navigation system
- URL-based parameter passing for QR code functionality
- Session state backup for navigation via sidebar

## Customization

### Adding More AE IDs
Edit the `ae_options` list in `Home.py`:
```python
ae_options = ["AE-0001", "AE-0002", "AE-0003", "AE-0004", "AE-0005"]
```

### Modifying QR Code URL
Update the `base_url` in the `generate_qr_code` function in `Home.py`:
```python
base_url = "your-domain.com/Page_2"  # For production deployment
```

### Styling
- Modify the Streamlit configuration in both files
- Add custom CSS using `st.markdown()` with HTML/CSS
- Adjust layout columns and spacing as needed

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed via `pip install -r requirements.txt`

2. **QR Code Not Working**: 
   - Ensure the base URL in the QR code matches your deployment URL
   - Check that Page_2.py is in the `pages/` directory

3. **Navigation Issues**:
   - Use `st.switch_page()` for programmatic navigation
   - Ensure page files are named correctly

### Development Notes

- The app uses Streamlit's experimental query params feature
- Session state is used as a fallback for navigation
- QR codes are generated in-memory and displayed directly

## License

This project is open source and available under the MIT License.
