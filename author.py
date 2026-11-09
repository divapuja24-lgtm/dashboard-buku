
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
        Developed by <span class="author-name">Group 9</span>
    </div>
    """)


def show_contributors():
    st.html("""
    <style>
    .contributors-section {
        max-width: 1050px;
        margin: 55px auto 20px auto;
        padding: 30px;
        background: #172438;
        border: 1px solid #263B54;
        border-top: 3px solid #35C6B4;
        border-radius: 16px;
        font-family: sans-serif;
        text-align: center;
        box-sizing: border-box;
    }

    .contributors-title {
        color: #35C6B4;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .contributors-subtitle {
        color: #9CAFC5;
        font-size: 12px;
        margin-bottom: 25px;
    }

    .contributors-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 15px;
    }

    .contributor-card {
        background: #0E192B;
        border: 1px solid #2B405A;
        border-radius: 12px;
        padding: 22px 12px;
        color: #E8EEF7;
        font-size: 13px;
        line-height: 1.6;
        min-height: 105px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow-wrap: anywhere;
    }

    .contributor-number {
        color: #35C6B4;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    .contributor-name {
        font-weight: 600;
    }

    .contributors-footer {
        margin-top: 22px;
        color: #9CAFC5;
        font-size: 11px;
        letter-spacing: 2px;
    }

    @media (max-width: 600px) {
        .contributors-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>

    <div class="contributors-section">
        <div class="contributors-title">
            PROJECT CONTRIBUTORS
        </div>

        <div class="contributors-subtitle">
            Meet the team behind this project
        </div>

        <div class="contributors-grid">

            <div class="contributor-card">
                <div class="contributor-number">MEMBER 01</div>
                <div class="contributor-name">
                    Diva Puja Prasetyawati
                </div>
            </div>

            <div class="contributor-card">
                <div class="contributor-number">MEMBER 02</div>
                <div class="contributor-name">
                    Aulia Vonna
                </div>
            </div>

            <div class="contributor-card">
                <div class="contributor-number">MEMBER 03</div>
                <div class="contributor-name">
                    Rohviska Novilita Marfilyamin
                </div>
            </div>

        </div>

        <div class="contributors-footer">
            GROUP 9 · DATA SCIENCE PROJECT
        </div>
    </div>
    """)
