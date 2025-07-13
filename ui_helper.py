import streamlit as st


class UIHelper:
    """Helper class for UI styling and components."""

    def load_custom_css(self):
        """Load custom CSS for enhanced UI design."""
        st.markdown("""
        <style>
        /* Main theme colors */
        .main {
            background-color: #fafafa;
        }

        /* Custom button styling */
        .stButton > button {
            background: linear-gradient(90deg, #1f77b4, #17a2b8);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #17a2b8, #1f77b4);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
        }

        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa;
        }

        /* Progress bar styling */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #1f77b4, #17a2b8);
        }

        /* File uploader styling */
        .stFileUploader > div {
            border: 2px dashed #1f77b4;
            border-radius: 10px;
            padding: 2rem;
            background-color: #f8f9fa;
        }
        </style>
        """, unsafe_allow_html=True)
