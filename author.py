
import streamlit as st

def show_author():
    st.markdown("""
    <style>
    .author-card {
        position: fixed;
        bottom: 15px;
        left: 20px;
        z-index: 9999;
        background: #172438;
        color: #E8EEF7;
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #35C6B4;
        font-family: sans-serif;
        font-size: 12px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    .author-name {
        color: #35C6B4;
        font-weight: bold;
    }

    .author-label {
        color: #9CAFC5;
        font-size: 10px;
        margin-top: 5px;
        margin-bottom: 3px;
        letter-spacing: 1px;
    }
    </style>

    <div class="author-card">
    <div>Developed by <span class="author-name">Group 9</span></div>
    <div class="author-label">PROJECT CONTRIBUTORS</div>
    <div>Diva Puja Prasetyawati</div>
    <div>Aulia Vonna</div>
    <div>Rohviska Novilita Marfilyamin</div>
    </div>
    """, unsafe_allow_html=True)
