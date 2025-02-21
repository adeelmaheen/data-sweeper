import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# App Title
st.set_page_config(page_title='Data Sweeper', layout='wide')
st.title("📊 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# User Name Input
name = st.sidebar.text_input("Enter Your Name:")
if name:
    st.sidebar.success(f"Welcome, {name}!")

# File Upload Section
uploaded_file = st.sidebar.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read file based on extension
        file_name = uploaded_file.name
        file_size = uploaded_file.size / 1024  # Convert bytes to KB
        
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.subheader(f"Uploaded Files by {name}")
        st.write(f"**File Name:** {file_name}")
        st.write(f"**File Size:** {file_size:.2f} KB")
        st.write("**Preview:**")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader(f"Data Cleaning for {file_name}")
        clean_data = st.checkbox(f"Clean Data for {file_name}")
        
        # Column Selection
        st.subheader(f"Select Columns for {file_name}")
        selected_columns = st.multiselect("Choose Columns", df.columns.tolist(), default=df.columns.tolist())
        df = df[selected_columns]
        
        # Visualization Options
        st.subheader(f"Visualization for {file_name}")
        show_chart = st.checkbox(f"Show Bar Chart for {file_name}")
        
        if show_chart and not df.select_dtypes(include=['number']).empty:
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            selected_column = st.selectbox("Select column for Bar Chart:", numeric_columns)
            fig, ax = plt.subplots()
            df[selected_column].value_counts().plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
            ax.set_title(f"Bar Chart of {selected_column}")
            st.pyplot(fig)
        elif show_chart:
            st.warning("No numeric columns available for visualization.")
        
        # File Conversion
        st.subheader(f"Convert {file_name}")
        conversion_type = st.radio(f"Convert {file_name} to:", ["CSV", "Excel"])
        
        if st.button(f"Convert {file_name}"):
            output_buffer = io.BytesIO()
            if conversion_type == "CSV":
                df.to_csv(output_buffer, index=False)
                output_buffer.seek(0)
                st.download_button("Download CSV", output_buffer, file_name=f"converted_{file_name}.csv", mime="text/csv")
            else:
                df.to_excel(output_buffer, index=False, engine="openpyxl")
                output_buffer.seek(0)
                st.download_button("Download Excel", output_buffer, file_name=f"converted_{file_name}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    except Exception as e:
        st.error(f"Error loading file: {e}")
