import platform
import subprocess
import tempfile

import streamlit as st
from utils.pdf_processing import extract_tables, table_to_image

# Streamlit App
st.title("Pathways Task Reminder")

os_info = platform.uname()
st.write(f"Operating System: {os_info.system}")
st.write(f"Node Name: {os_info.node}")
st.write(f"Release: {os_info.release}")
st.write(f"Version: {os_info.version}")
st.write(f"Machine: {os_info.machine}")
st.write(f"Processor: {os_info.processor}")


def check_tool_availability(tool_name):
    try:
        result = subprocess.run(
            [tool_name, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode().strip()
    except FileNotFoundError:
        return f"{tool_name} is not available."
    except subprocess.CalledProcessError:
        return f"{tool_name} is available but returned an error."


tools = ["git", "curl", "wget", "python", "pdftotext"]
for tool in tools:
    st.write(check_tool_availability(tool))


# File uploader
uploaded_file = st.file_uploader(
    "Upload your Pathways Student Summary PDF", type=["pdf"]
)
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Extract tables from the PDF
    tables = extract_tables(temp_file_path)

    if not tables:
        st.error("No tables found in the uploaded PDF.")
    else:
        st.success(f"Found {len(tables)} tables in the PDF!")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
        table_image_path = temp_image_file.name
        table_to_image(
            tables[0], output_path=table_image_path
        )  # Save image to temp file

        # Display the image
        st.image(table_image_path, caption="First Table", use_container_width=True)

        # Allow download of the image
        with open(table_image_path, "rb") as img_file:
            st.download_button(
                label="Download Table Image",
                data=img_file,
                file_name="table_image.png",
                mime="image/png",
            )
