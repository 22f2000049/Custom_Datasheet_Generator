import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Product Data Entry App", layout="wide")
st.title("🧾 Product Data Entry")

# Step 1: Upload CSV template
uploaded_file = st.file_uploader("📂 Upload product template CSV", type="csv")

if uploaded_file:
    # Load CSV headers
    df_template = pd.read_csv(uploaded_file, nrows=0)
    fields = df_template.columns.tolist()

    # Manually define grouped fields
    grouped_fields = {
        "Basic Info": ['item_code', 'description', 'description_2', 'search_description'],
        "Status Flags": ['sellable', 'purchasable', 'obsolete', 'discontinued'],
        "Website Availability": ['website_available', 'beta_website_available', 'website_associated_available'],
        "Physical Specs": ['length', 'width', 'height', 'product_weight_net', 'product_weight_gross'],
        "Electrical Specs": ['dc_voltage', 'ac_voltage', 'current', 'power_consumption'],
        "Lighting Specs": ['lumen', 'colour_temperature', 'cri', 'R9'],
        "Temperature Specs": ['operating_temperature', 'storage_temperature']
    }

    # Flatten all grouped field names
    grouped_field_names = [field for sublist in grouped_fields.values() for field in sublist]

    # Add remaining fields to "Other Fields"
    grouped_fields["Other Fields"] = [f for f in fields if f not in grouped_field_names]

    # Step 2: Init session storage
    if "product_data" not in st.session_state:
        st.session_state.product_data = []

    # Step 3: Dynamic form
    with st.form("product_form"):
        st.subheader("📝 Enter Product Info")
        new_entry = {}

        for section, section_fields in grouped_fields.items():
            with st.expander(section, expanded=(section == "Basic Info")):
                cols = st.columns(2)
                for i, field in enumerate(section_fields):
                    with cols[i % 2]:
                        value = st.text_input(field)
                        if value.strip() != "":
                            new_entry[field] = value

        if st.form_submit_button("➕ Add Product Row"):
            st.session_state.product_data.append(new_entry)
            st.success("✅ Product row added!")

    # Step 4: Preview + download
    if st.session_state.product_data:
        st.subheader("📋 Preview of Entered Products")
        df = pd.DataFrame(st.session_state.product_data).fillna("")
        st.dataframe(df)

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        st.download_button(
            label="📥 Download CSV (without empty fields)",
            data=csv_buffer.getvalue(),
            file_name="filled_products.csv",
            mime="text/csv"
        )
else:
    st.info("👆 Upload a CSV file to get started.")
