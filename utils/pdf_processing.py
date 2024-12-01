import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt

def extract_tables(pdf_path):
    """Extracts tables from a PDF file using pdfplumber."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables as pandas DataFrames
            page_tables = page.extract_tables()
            for table in page_tables:
                df = pd.DataFrame(table[1:], columns=table[0])  # Use the first row as header
                tables.append(df)
    return tables

def table_to_image(table, output_path="table_image.png"):
    """Converts a DataFrame table into an image."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    ax.axis("tight")
    ax.table(cellText=table.values, colLabels=table.columns, loc="center")

    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return output_path
