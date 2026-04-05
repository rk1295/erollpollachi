import streamlit as st
import pandas as pd

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("database.xlsx")
    df.columns = df.columns.str.strip()
    df["PartNo"] = df["PartNo"].astype(str)
    df["SerialNo"] = df["SerialNo"].astype(str)
    return df

df = load_data()

# -------------------------------
# Page Title
# -------------------------------
st.title("Elector Search")

# -------------------------------
# CSS: Force side-by-side on mobile
# -------------------------------
st.markdown("""
<style>

/* Force columns to stay side-by-side */
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
}

/* Ensure equal width columns */
div[data-testid="column"] {
    flex: 1 1 0% !important;
    min-width: 0 !important;
    max-width: 50% !important;
    padding: 0px 4px !important;
}

/* Compact input box */
input {
    text-align: center;
    padding: 6px !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Input Section (10 rows)
# -------------------------------
inputs = []

for i in range(10):
    cols = st.columns(2)

    part = cols[0].text_input(
        label=f"P{i+1}",
        key=f"part{i}",
        placeholder="Part",
        max_chars=4
    )

    serial = cols[1].text_input(
        label=f"S{i+1}",
        key=f"serial{i}",
        placeholder="Serial",
        max_chars=4
    )

    if part and serial:
        inputs.append((part, serial))

# -------------------------------
# Search Button
# -------------------------------
if st.button("Search"):
    if inputs:
        input_df = pd.DataFrame(inputs, columns=["PartNo", "SerialNo"])

        result = input_df.merge(
            df[["PartNo", "SerialNo", "Elector's Name"]],
            on=["PartNo", "SerialNo"],
            how="left"
        )

        result["Elector's Name"] = result["Elector's Name"].fillna("Not Found")

        st.success("Results")
        st.dataframe(result, use_container_width=True)

    else:
        st.warning("Enter at least one record")