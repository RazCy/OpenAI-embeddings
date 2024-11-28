import pandas as pd

def convert_excel_to_sql(excel_file, output_file, table_name):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Open the output file to write SQL statements
    with open(output_file, "w") as file:
        for _, row in df.iterrows():
            # Prepare values for SQL insertion
            values = ", ".join(
                f"'{str(val).replace("'", "''")}'" if pd.notna(val) else "NULL"
                for val in row
            )
            
            # Create an INSERT statement
            sql_statement = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});"
            file.write(sql_statement + "\n")
    
    print(f"SQL insert statements written to {output_file}")

# Usage example
excel_file_path = "path_to_your_excel_file.xlsx"
output_file_path = "insert_statements.sql"
table_name = "app_inventory"

convert_excel_to_sql(excel_file_path, output_file_path, table_name)
