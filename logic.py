import pandas as pd
import os

def process_invoice_file(input_path, output_path):
    # Read the Excel file, skip the first row (contains POM info)
    df = pd.read_excel(input_path, skiprows=1)

    # Clean column names
    df.columns = df.columns.str.strip()

    print("Columns found:", df.columns.tolist())

    # Extract POM from the first row manually
    pom_df = pd.read_excel(input_path, nrows=1, header=None)
    pom_raw = pom_df.iloc[0, 0]
    if isinstance(pom_raw, str) and "POM:" in pom_raw:
        pom_value = pom_raw.split("POM:")[1].strip()
    else:
        pom_value = None

    # Check if required columns exist
    required_columns = ["S.No", "Tax", "Total Value", "Manufacture Address"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Handle missing or zero tax
    df["Tax"] = pd.to_numeric(df["Tax"], errors="coerce").fillna(0)
    df["EWB"] = df["Tax"].apply(lambda x: "NA" if x == 0 else "ToCheck")

    # Calculate total turnover (include all rows even with Tax=0)
    total_turnover = df["Total Value"].sum()

    # Apply Inter/Intra state logic only for rows where Tax != 0
    def assign_ewb(row):
        if row["EWB"] == "NA":
            return "NA"
        elif pom_value is not None and str(row["Manufacture Address"]).strip() != pom_value:
            return "A"  # Interstate
        else:
            return "A" if total_turnover >= 50000 else "NA"

    df["EWB"] = df.apply(assign_ewb, axis=1)

    # Save to Excel
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)

