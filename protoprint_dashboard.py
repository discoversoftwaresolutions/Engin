import streamlit as st

st.title("ProtoPrint - Additive Manufacturing")
st.write("Simulate, slice, and recommend materials for 3D printing workflows.")

uploaded_stl = st.file_uploader("Upload STL File", type=["stl"])
if uploaded_stl:
    st.success(f"File '{uploaded_stl.name}' uploaded.")
    st.selectbox("Material", ["PLA", "ABS", "PETG", "Nylon", "Resin"])
    st.slider("Layer Height (mm)", 0.05, 0.3, 0.1)
    st.button("Simulate Print Path")
    st.button("Run Material Recommendation")
    st.text_area("Print Summary", height=200)

st.markdown("#### Print Preview")
st.checkbox("Show temperature zones")
st.checkbox("Enable print time estimation")
