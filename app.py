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

    st.text(
        "HINTS: If on phone can press on an image and then share to texting application. If on computer, can drag and drop images directly into texting applications. Download functionality is provided if you want to save them all."
    )
    for name, image_path in image_paths_by_name.items():
        st.divider()

        # Display the image
        st.image(str(image_path), caption=name, use_container_width=False)

        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
            st.download_button(
                label=f"Download {name} report",
                data=image_bytes,
                file_name=f"{name.replace(' ', '_')}.png",
                mime="image/png",
            )

        st.text("")
