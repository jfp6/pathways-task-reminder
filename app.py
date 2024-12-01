import streamlit as st
from utils.pdf_processing import extract_tables, table_to_image

# Streamlit App
st.title("PDF Table Extractor and Image Converter")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    # Save uploaded file to disk
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract tables from the PDF
    tables = extract_tables("uploaded.pdf")

    if not tables:
        st.error("No tables found in the uploaded PDF.")
    else:
        st.success(f"Found {len(tables)} tables in the PDF!")

        # Convert the first table to an image
        table_image_path = table_to_image(tables[0])

        # Display the image
        st.image(table_image_path, caption="First Table", use_column_width=True)

        # Provide download link
        with open(table_image_path, "rb") as img_file:
            st.download_button(
                label="Download Table Image",
                data=img_file,
                file_name="table_image.png",
                mime="image/png",
            )
