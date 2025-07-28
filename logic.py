import pandas as pd
import re

def process_invoice_file(input_path, output_path):
    df = pd.read_excel(input_path, skiprows=1)
    pom_row = pd.read_excel(input_path, nrows=1).columns[0]

    match = re.search(r'POM\s*:\s*(.+)', pom_row)

    if match:
        pom = match.group(1).strip()
    else:
        raise ValueError("POM not found in the first row of the Excel file.")

    df.columns = [col.strip() for col in df.columns]
    df['EWB'] = 'NA'
    taxable_mask = df['Tax'] != 0
    taxable_total_sum = df.loc[taxable_mask, 'Total Value'].sum()

    for i, row in df.iterrows():
        tax = row['Tax']
        if tax == 0:
            df.at[i, 'EWB'] = 'NA'
        else:
            manuf_addr = str(row['Manufacture Address']).strip()
            if manuf_addr != pom:
                df.at[i, 'EWB'] = 'A'
            else:
                df.at[i, 'EWB'] = 'A' if taxable_total_sum >= 50000 else 'NA'

    df.to_excel(output_path, index=False)
