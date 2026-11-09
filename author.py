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
    """, unsafe_allow_html=True)


def show_contributors():
    st.markdown("""
    <div style="
        margin-top: 50px;
        padding: 22px;
        background: #172438;
        border-top: 2px solid #35C6B4;
        border-radius: 10px;
        color: #E8EEF7;
        text-align: center;
        font-family: sans-serif;
    ">
        <div style="
            color: #35C6B4;
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 12px;
        ">
            PROJECT CONTRIBUTORS
        </div>

        <div style="font-size: 13px; line-height: 2;">
            Diva Puja Prasetyawati<br>
            Aulia Vonna<br>
            Rohviska Novilita Marfilyamin
        </div>

        <div style="
            margin-top: 12px;
            color: #9CAFC5;
            font-size: 11px;
        ">
            Group 9
        </div>
    </div>
    """, unsafe_allow_html=True)
