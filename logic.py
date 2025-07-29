import pandas as pd
import re

def process_invoice_file(input_path: str, output_path: str):
    # Read Excel file
    df = pd.read_excel(input_path)

    # Extract 'Place of Manufacture' (POM)
    with open(input_path, 'rb') as f:
        excel_file = pd.ExcelFile(f)
        try:
            first_sheet = pd.read_excel(excel_file, sheet_name=0, nrows=5, header=None)
        except Exception:
            raise ValueError("Unable to read the Excel file header.")

    pom = None
    for row in first_sheet[0]:
        if isinstance(row, str) and "POM:" in row:
            match = re.search(r'POM:\s*(.*)', row)
            if match:
                pom = match.group(1).strip()
                break

    if not pom:
        raise ValueError("POM not found in the first few rows of the Excel file.")

    # Check required columns exist
    required_cols = ["S.No", "invoice number", "Date", "Name", "Total Value", "Tax", "Manufacture Address"]
    for col in required_cols:
        print("Columns found:", df.columns.tolist())
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Convert column names to consistent format
    df["EWB"] = "NA"  # Default to NA

    # Step 1: Mark all Tax == 0 as NA (also included in total sum)
    # (done by default above)

    # Step 2: Get total sum of Total Value (including Tax == 0)
    total_sum = df["Total Value"].sum()

    # Step 3: Go row by row for EWB logic
    for index, row in df.iterrows():
        if row["Tax"] == 0:
            df.at[index, "EWB"] = "NA"
        else:
            manu_address = str(row["Manufacture Address"]).strip()
            if manu_address != pom:
                df.at[index, "EWB"] = "A"  # Inter-state
            else:
                if total_sum >= 50000:
                    df.at[index, "EWB"] = "A"
                else:
                    df.at[index, "EWB"] = "NA"

    # Save final file
    df.to_excel(output_path, index=False)
