import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class Style:
    @staticmethod
    def titre(encoded_image, text) -> DeltaGenerator:
        """Generate a styled header for a real estate sale agreement.

        This function generates and returns a styled HTML header containing a title and an image.
        The header is styled using CSS and the image is displayed using a base64 encoded string.

        Args:
            encoded_image (str): Base64 encoded image string to be displayed in the header.
            text (str): Title of the page to be dispalyed in the header

        Returns:
            DeltaGenerator: Streamlit object representing the styled header.
        """
        style = st.markdown(
            f"""
            <style>
            .header-container {{
                display: flex;
                align-items: center;
                justify-content: center; /* Center horizontally */
                margin-bottom: 50px;  /* Add space below the container */
            }}
            .header-text {{
                font-size: 2.2em;  /* Increase font size */
                margin: 0;  /* Remove any margin */
            }}
            .header-image img {{
                width: 55px;
                margin-left: 10px;  /* Add some space between text and image */
            }}
            </style>
            <div class="header-container">
                <div class="header-text"><b>{text}</b></div>
                <div class="header-image"><img src="data:image/png;base64,{encoded_image}" alt="Maison"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return style

    @staticmethod
    def spinner() -> str:
        """Generate the CSS for a loading spinner.

        This function generates and returns a string containing CSS styles for a loading spinner.
        The spinner is styled as a small, rotating circle with specific dimensions and colors.

        Returns:
            str: CSS styles for a loading spinner.
        """
        loader_style = """
        <style>
        #loader {
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 15px;
            height: 15px;
            border-radius: 50%;
            border-left-color: #3498db;
            animation: spin 1s ease infinite;
            display: inline-block;
            margin-left: 10px;
            margin-bottom: -2px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """
        return loader_style
