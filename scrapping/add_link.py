import streamlit as st
import pandas as pd
import os

CSV_FILE = "pdf_list.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["link", "file_name"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

st.set_page_config(page_title="PDF Dataset Manager", layout="wide")
st.title("📚 AfroPharmacopoeia PDF Manager")

df = load_data()

# Add new entry
with st.form("add_entry", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        link = st.text_input("PDF Link (URL)")
    with col2:
        file_name = st.text_input("File Name (e.g., plant_study.pdf)")
    submitted = st.form_submit_button("➕ Add")

    if submitted and link:
        new_row = pd.DataFrame([{
                "link": link,
                "file_name": file_name if file_name else link.split("/")[-1]
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("✅ Added successfully!")

# Display CSV
st.divider()
st.subheader("📄 Current Dataset")
st.dataframe(df, width='stretch', hide_index=True)

# Download button
if not df.empty:
    st.download_button(
            label="📥 Download CSV",
            data=df.to_csv(index=False),
            file_name="pdf_list.csv",
            mime="text/csv"
    )