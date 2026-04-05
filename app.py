import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("database.xlsx")
    df.columns = df.columns.str.strip()
    df["PartNo"] = df["PartNo"].astype(str)
    df["SerialNo"] = df["SerialNo"].astype(str)
    return df

df = load_data()

st.title("Elector Search")

# CSS for compact inputs
st.markdown("""
<style>
/* Reduce input box height and padding */
input {
    text-align: center;
    padding: 4px !important;
}

/* Make columns tighter */
div[data-testid="column"] {
    padding: 0px 5px !important;
}
</style>
""", unsafe_allow_html=True)

inputs = []

for i in range(10):
    cols = st.columns([1,1], gap="small")
    
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

# Search
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
        st.warning("Enter at least one record")