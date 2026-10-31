
from html import escape
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import json
import sqlite3

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import database as db

from matching import suggest_matches
from validation import (
    validate_file,
    INVOICE_COLUMNS,
    PAYMENT_COLUMNS,
)
from finance_features import (
    initialize_features,
    get_activity,
    get_invoice_age_report,
    load_matching_data,
    parse_money,
    review_match,
    run_integrity_checks,
)


st.set_page_config(
    page_title="ReconFlow | Intelligence Workspace",
    page_icon="◈",
    layout="wide",
)

try:
    initialize_features()
except Exception as exc:
    st.error(f"Initialization failed: {exc}")
    st.stop()


# -------------------- DESIGN --------------------

st.html("""
<style>
.stApp {
    background:
        radial-gradient(
            ellipse at 90% 0%,
            rgba(124, 92, 255, .13),
            transparent 38%
        ),
        #0B1020;
}
.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 { letter-spacing: -.035em; }

.brand {
    font-size: 29px;
    font-weight: 850;
    color: #F5F6FF;
    letter-spacing: -.06em;
}
.brand span { color: #A99AFF; }
.brand-sub {
    color: #8895B5;
    font-size: 10px;
    letter-spacing: .2em;
    margin: 4px 0 26px;
}
.hero {
    padding: 30px;
    margin-bottom: 24px;
    border: 1px solid rgba(167, 146, 255, .22);
    border-radius: 24px;
    background: linear-gradient(
        115deg, #151E38, #25224B 65%, #443477
    );
    box-shadow: 0 20px 55px rgba(0,0,0,.16);
}
.eyebrow {
    color: #BDB0FF;
    letter-spacing: .17em;
    font-size: 10px;
    font-weight: 750;
}
.hero h1 {
    color: #FFFFFF;
    font-size: clamp(28px, 3vw, 42px);
