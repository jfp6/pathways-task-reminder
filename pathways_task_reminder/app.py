from pathlib import Path
import tempfile

import streamlit as st
from pathways_task_reminder.student_reporter import StudentReporter

# Streamlit App
st.title("Pathways Task Reminder")

uploaded_file = st.file_uploader(
    "Upload your Pathways Student Summary PDF", type=["pdf"]
)
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        pdf_file_path = Path(temp_file.name)

    image_paths_by_name = StudentReporter.create_images_from_pdf(pdf_file_path)

    if not image_paths_by_name:
        st.error("No tables found in the uploaded PDF.")
    else:
        st.success(f"Found {len(image_paths_by_name)} tables in the PDF!")

    for name, image_path in image_paths_by_name.items():
        st.image(image_path, caption=name, use_container_width=True)

        # with open(table_image_path, "rb") as img_file:
        #     st.download_button(
        #         label="Download Table Image",
        #         data=img_file,
        #         file_name="table_image.png",
        #         mime="image/png",
        #     )
