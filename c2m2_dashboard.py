import streamlit as st
import pandas as pd
import io

def load_data(file_path):
    """Loads Excel data into a DataFrame with error handling for missing or incorrect sheet names."""
    try:
        df = pd.read_excel(file_path, sheet_name='C2M2 V2.1')
        return df
    except ValueError:
        st.error("Error: The sheet 'C2M2 V2.1' was not found in the uploaded Excel file. Please ensure the correct sheet is present.")
        return pd.DataFrame()  # Return an empty DataFrame to avoid crashes.
    except Exception as e:
        st.error(f"An unexpected error occurred while reading the file: {e}")
        return pd.DataFrame()

def download_sample_template():
    """Generates a sample Excel template for users to download."""
    sample_data = {
        'Domain': ['Sample Domain 1', 'Sample Domain 2'],
        'Module': ['Sample Module 1', 'Sample Module 2'],
        'MIL': [1, 2],
        'Objective': ['Sample Objective 1', 'Sample Objective 2'],
        'Practice Text': ['Sample Practice Text 1', 'Sample Practice Text 2'],
        'Artifacts': ['Sample Artifact 1', 'Sample Artifact 2'],
        'CSF V1.1 Mapping': ['Sample CSF 1', 'Sample CSF 2'],
        'CSF V2.0 Mapping': ['Sample CSF 1.1', 'Sample CSF 2.1'],
        'Help Text': ['Sample Help Text 1', 'Sample Help Text 2']
    }
    df = pd.DataFrame(sample_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='C2M2 V2.1')
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("C2M2 Data Interactive Dashboard")
    st.write("Select and filter data based on your preferences.")

    # Add a button to download a sample Excel template
    st.sidebar.write("### Download Sample Template")
    sample_template = download_sample_template()
    st.sidebar.download_button(
        label="Download Sample Excel Template",
        data=sample_template,
        file_name="C2M2_Sample_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # File upload section
    uploaded_file = st.file_uploader("Upload the C2M2 Excel file", type=["xlsx"])
    if uploaded_file is not None:
        st.write(f"**Uploaded File:** {uploaded_file.name}")
        df = load_data(uploaded_file)

        if df.empty:
            st.warning("No data to display. Please upload a valid Excel file with the correct sheet name.")
            return

        # Sidebar Filters
        st.sidebar.header("Filters")
        domain_filter = st.sidebar.multiselect("Select Domain", options=df["Domain"].unique(), default=df["Domain"].unique())
        module_filter = st.sidebar.multiselect("Select Module", options=df["Module"].unique(), default=df["Module"].unique())
        mil_filter = st.sidebar.multiselect("Select MIL", options=df["MIL"].unique(), default=df["MIL"].unique())
        objective_filter = st.sidebar.text_input("Search Objective", "")
        practice_text_filter = st.sidebar.text_input("Search Practice Text", "")

        # Filter Data
        filtered_data = df[
            (df["Domain"].isin(domain_filter)) &
            (df["Module"].isin(module_filter)) &
            (df["MIL"].isin(mil_filter)) &
            (df["Objective"].str.contains(objective_filter, case=False, na=False)) &
            (df["Practice Text"].str.contains(practice_text_filter, case=False, na=False))
        ]

        # Main Data Display
        st.write("### Filtered Data", filtered_data)

        # Download filtered data
        st.download_button(
            label="Download Filtered Data as Excel",
            data=filtered_data.to_excel(index=False, engine='openpyxl'),
            file_name="filtered_c2m2_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.write("Please upload the C2M2 Excel file to proceed.")

if __name__ == "__main__":
    st.write("## Streamlit Cloud Setup Instructions")
    st.markdown(
        """### To Deploy This App from GitHub:
        1. Go to **[Streamlit Cloud](https://share.streamlit.io)**.
        2. Click **Sign In** and log in with GitHub.
        3. Click **Deploy a Public App from GitHub**.
        4. Connect your GitHub repository containing `c2m2_dashboard.py`.
        5. In the **Branch** field, select your main branch.
        6. In the **Main File Path** field, type `c2m2_dashboard.py`.
        7. Click **Deploy**.

        **Note:** If you do not have a GitHub repo, create one and upload your script file there.

        Once the app is deployed, Streamlit Cloud will provide you with a shareable public URL.

        ### No GitHub? Upload Directly:
        - Use **Streamlit Community Templates** or **drag your script into their upload area**.
        - Alternatively, use **Replit** or **Google Colab** for quick cloud-based development.

        """)
    main()
