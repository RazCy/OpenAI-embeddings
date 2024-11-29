import pandas as pd

def convert_excel_to_sql(excel_file, output_file, table_name):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
 # Open the output file to write SQL statements
with open(output_file, "w", encoding="utf-8") as file:
    for _, row in df.iterrows():
        # Prepare values for SQL insertion with special character escaping
        escaped_values = []
        for val in row:
            if pd.notna(val):
                if isinstance(val, str):
                    # Escape single quotes and backslashes
                    escaped_value = val.replace("'", "''").replace("\\", "\\\\")
                    escaped_values.append(f"'{escaped_value}'")
                else:
                    # Keep numeric or other values as they are
                    escaped_values.append(str(val))
            else:
                # Handle NULL values
                escaped_values.append("NULL")
        
        # Create an INSERT statement
        sql_statement = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(escaped_values)});"
        file.write(sql_statement + "\n")

    
    print(f"SQL insert statements written to {output_file}")

# Usage example
excel_file_path = "path_to_your_excel_file.xlsx"
output_file_path = "insert_statements.sql"
table_name = "app_inventory"

convert_excel_to_sql(excel_file_path, output_file_path, table_name)
