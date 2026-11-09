
import streamlit as st


def show_author():
    st.html("""
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
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    .author-name {
        color: #35C6B4;
        font-weight: bold;
    }
    </style>

    <div class="author-card">
        Developed by
        <span class="author-name">Group 9</span>
    </div>
    """)



def show_contributors():
    st.html("""
    <style>
    .contributors-section {
        margin: 25px auto 5px auto;
        padding: 14px 10px;
        background: #172438;
        border-top: 1px solid #2B405A;
        border-radius: 8px;
        font-family: sans-serif;
        text-align: center;
    }

    .contributors-grid {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px 30px;
    }

    .contributor-name {
        color: #B9C8DA;
        font-size: 11px;
        font-weight: 500;
    }
    </style>

    <div class="contributors-section">
        <div class="contributors-grid">
            <div class="contributor-name">
                Diva Puja Prasetyawati
            </div>

            <div class="contributor-name">
                Aulia Vonna
            </div>

            <div class="contributor-name">
                Rohviska Novilita Marfilyamin
            </div>
        </div>
    </div>
    """)

