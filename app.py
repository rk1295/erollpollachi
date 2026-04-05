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

st.title("Elector Search")

# -------------------------------
# CSS: Make inputs SMALL
# -------------------------------
st.markdown("""
<style>

/* Force side-by-side */
div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
}

/* Make columns tight */
div[data-testid="column"] {
    max-width: 80px !important;
    flex: 1 1 80px !important;
}

/* Make input boxes small */
input {
    width: 70px !important;
    text-align: center;
    padding: 4px !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Input Section
# -------------------------------
inputs = []

for i in range(10):
    cols = st.columns(2)

    part = cols[0].text_input(
        f"P{i+1}",
        key=f"part{i}",
        max_chars=4
    )

    serial = cols[1].text_input(
        f"S{i+1}",
        key=f"serial{i}",
        max_chars=4
    )

    # Ensure numeric only
    if part.isdigit() and serial.isdigit():
        inputs.append((part, serial))

# -------------------------------
# Search
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

        st.dataframe(result, use_container_width=True)
    else:
        st.warning("Enter valid numeric values")