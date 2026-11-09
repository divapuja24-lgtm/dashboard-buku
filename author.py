
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
        width: 100%;
        box-sizing: border-box;
        margin: 35px auto 10px auto;
        padding: 20px 24px;
        background: #172438;
        border: 1px solid #263B54;
        border-top: 2px solid #35C6B4;
        border-radius: 12px;
        font-family: sans-serif;
        text-align: center;
    }

    .contributors-title {
        color: #35C6B4;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .contributors-subtitle {
        color: #9CAFC5;
        font-size: 11px;
        margin-bottom: 17px;
    }

    .contributors-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }

    .contributor-card {
        background: #0E192B;
        border: 1px solid #2B405A;
        border-radius: 9px;
        padding: 13px 8px;
        color: #E8EEF7;
        font-size: 12px;
        line-height: 1.5;
        min-height: 65px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow-wrap: anywhere;
    }

    .contributor-number {
        color: #35C6B4;
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }

    .contributor-name {
        font-weight: 600;
    }

    .contributors-footer {
        margin-top: 16px;
        color: #9CAFC5;
        font-size: 10px;
        letter-spacing: 1.2px;
        line-height: 1.6;
    }

    @media (max-width: 600px) {
        .contributors-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>

    <div class="contributors-section">

        <div class="contributors-title">
            PROJECT TEAM
        </div>

        <div class="contributors-subtitle">
            Group 9
        </div>

        <div class="contributors-grid">

            <div class="contributor-card">
                <div class="contributor-number">
                    MEMBER 01
                </div>
                <div class="contributor-name">
                    Diva Puja Prasetyawati
                </div>
            </div>

            <div class="contributor-card">
                <div class="contributor-number">
                    MEMBER 02
                </div>
                <div class="contributor-name">
                    Aulia Vonna
                </div>
            </div>

            <div class="contributor-card">
                <div class="contributor-number">
                    MEMBER 03
                </div>
                <div class="contributor-name">
                    Rohviska Novilita Marfilyamin
                </div>
            </div>

        </div>

        <div class="contributors-footer">
            DEPARTEMEN STATISTIKA<br>
            INSTITUT TEKNOLOGI SEPULUH NOPEMBER
        </div>

    </div>
    """)
