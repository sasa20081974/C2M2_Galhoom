import streamlit as st
import pandas as pd

def load_data(file_path):
    """Loads Excel data into a DataFrame."""
    df = pd.read_excel(file_path, sheet_name='C2M2 V2.1')
    return df

def main():
    st.title("C2M2 Data Interactive Dashboard")
    st.write("Select and filter data based on your preferences.")

    # File upload section
    uploaded_file = st.file_uploader("Upload the C2M2 Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)

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
