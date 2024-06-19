import streamlit as st


def titre(encoded_image):

    style = st.markdown(
        f"""
        <style>
        .header-container {{
            display: flex;
            align-items: center;
        }}
        .header-text {{
            font-size: 2em;
            margin-right: 10px;  /* Adjust this value to control the space between text and image */
        }}
        .header-image img {{
            width: 50px;
        }}
        </style>
        <div class="header-container">
            <div class="header-text">Compromis de vente immobilier</div>
            <div class="header-image"><img src="data:image/png;base64,{encoded_image}" alt="Maison"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return style


def spinner():
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
