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

st.title("Bulk Elector Search")

# Create 10 input rows
inputs = []

for i in range(10):
    col1, col2 = st.columns(2)
    part = col1.text_input(f"PartNo {i+1}", key=f"part{i}")
    serial = col2.text_input(f"SerialNo {i+1}", key=f"serial{i}")
    
    if part and serial:
        inputs.append((part, serial))

# Search button
if st.button("Search All"):
    if inputs:
        input_df = pd.DataFrame(inputs, columns=["PartNo", "SerialNo"])
        
        result = input_df.merge(
            df[["PartNo", "SerialNo", "Elector's Name"]],
            on=["PartNo", "SerialNo"],
            how="left"
        )
        
        result["Elector's Name"] = result["Elector's Name"].fillna("Not Found")
        
        st.dataframe(result)
    else:
        st.warning("Please enter at least one record")