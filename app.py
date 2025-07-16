import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Product Data Entry App", layout="wide")
st.title("🧾 Product Data Entry")

# Upload product template
uploaded_file = st.file_uploader("📂 Upload product template CSV", type="csv")

if uploaded_file:
    df_template = pd.read_csv(uploaded_file, nrows=0)
    fields = df_template.columns.tolist()

    # Custom placeholders with meaningful examples
    example_placeholders = {
        "item_code": "DIGSV186512_",
        "description": "DELTA IN-GROUND SV 1800-6500K 12W 360LM CRI80 IP67 IK10",
        "sellable": "1 (1 = Yes, 0 = No)",
        "purchasable": "1 (1 = Yes, 0 = No)",
        "obsolete": "0 (1 = Yes, 0 = No)",
        "discontinued": "0 (1 = Yes, 0 = No)",
        "colour_temperature": "3000 (Kelvin)",
        "operating_temperature": "-40°C to 55°C",
        "storage_temperature": "-10°C to 60°C",
        "connection": "255mm Cable with Male/Female Connectors",
        "mounting": "Mounting Brackets",
        "dc_voltage": "24",
        "current": "0.5 (Amps)",
        "power_consumption": "12 (Watts)",
        "lumen": "360",
        "cri": "80",
        "beam_angle": "120°",
    }

    # Group fields
    grouped_fields = {
        "Basic Info": ['item_code', 'description', 'description_2', 'search_description'],
        "Status Flags": ['sellable', 'purchasable', 'obsolete', 'discontinued'],
        "Website Availability": ['website_available', 'beta_website_available', 'website_associated_available'],
        "Physical Specs": ['length', 'width', 'height', 'product_weight_net', 'product_weight_gross'],
        "Electrical Specs": ['dc_voltage', 'ac_voltage', 'current', 'power_consumption'],
        "Lighting Specs": ['lumen', 'colour_temperature', 'cri', 'R9'],
        "Temperature Specs": ['operating_temperature', 'storage_temperature']
    }

    grouped_field_names = [f for sublist in grouped_fields.values() for f in sublist]
    grouped_fields["Other Fields"] = [f for f in fields if f not in grouped_field_names]

    if "product_data" not in st.session_state:
        st.session_state.product_data = []

    with st.form("product_form"):
        st.subheader("📝 Enter Product Info")
        new_entry = {}

        for section, section_fields in grouped_fields.items():
            with st.expander(section, expanded=(section == "Basic Info")):
                cols = st.columns(2)
                for i, field in enumerate(section_fields):
                    with cols[i % 2]:
                        placeholder = example_placeholders.get(field, "Enter value")
                        value = st.text_input(field, placeholder=placeholder)
                        if value.strip():
                            new_entry[field] = value

        if st.form_submit_button("➕ Add Product Row"):
            st.session_state.product_data.append(new_entry)
            st.success("✅ Product row added!")

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
    st.info("👆 Please upload a CSV file to begin.")
