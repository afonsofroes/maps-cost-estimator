"""
This script is used to load and apply CSS styles in a Streamlit application. It reads the CSS from a file and injects it into the Streamlit app to customise the appearance.

Example:
    To use this script, simply call the `load_css` function in your Streamlit app:

    ```python
    import streamlit as st
    from your_script_name import load_css

    load_css()
    ```

    Ensure that the CSS file is located in the `styles` directory relative to the script.
"""

import streamlit as st
from pathlib import Path

def load_css():
    """
    Load and apply CSS styles from the styles file.

    This function attempts to read a CSS file located in the `styles` directory
    relative to the script's location and injects the CSS into the Streamlit app.

    Raises
    ------
    FileNotFoundError
        If the CSS file does not exist.
    Exception
        If there is any other error while reading the CSS file or applying the styles.
    """
    try:
        # Get the absolute path to the styles directory
        current_dir = Path(__file__).resolve().parent
        css_file = current_dir / "styles" / "styles.css"

        # Check if the CSS file exists
        if css_file.exists():
            # Open and read the CSS file, then inject it into the Streamlit app
            with open(css_file) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            # Display an error message if the CSS file is not found
            st.error(f"CSS file not found at: {css_file}")
    except Exception as e:
        # Display an error message if there is an issue loading the CSS file
        st.error(f"Failed to load application styles: {str(e)}")
