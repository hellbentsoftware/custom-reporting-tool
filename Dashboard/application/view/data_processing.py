import pandas as pd
import base64
import io

def generate_summary_table(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    # Try to read the CSV file with different encodings if necessary
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except UnicodeDecodeError:
        df = pd.read_csv(io.StringIO(decoded.decode('ISO-8859-1')))
    
    # Generate the summary table (Total Sales, Total Quantity Ordered, and Average Price per Country)
    summary_table = df.groupby('COUNTRY').agg(
        Total_Sales=('SALES', 'sum'),
        Total_Quantity_Ordered=('QUANTITYORDERED', 'sum'),
        Avg_Price=('PRICEEACH', 'mean')
    ).reset_index()
    
    # Sort the table by Total Sales for better readability
    summary_table = summary_table.sort_values(by='Total_Sales', ascending=False)
    
    return summary_table
