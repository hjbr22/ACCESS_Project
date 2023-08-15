import pandas as pd



def validate_numeric_values(column):
    return pd.to_numeric(column, errors='coerce').notna().all()

def validate_table_1(table):
    # Validate values in Temp Storage column
   if not validate_numeric_values(table['Temp Storage (TB)']):
      return False, "Temp Storage (TB) column contains non-numeric values"
   elif not validate_numeric_values(table['Long-Term Storage (TB)']):
      return False, "Long-Term Storage (TB) column contains non-numeric values"
    
   return True

def validate_table_2(table):
   if not validate_numeric_values(table['Amount (GB)']):
      return False, "Memory (RAM) Node column contains non-numeric values"
   return True

def validate_table_3(table):
    # Validate values in Suitability column
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
    
    
   return True

def validate_table_4(table):
    # Validate values in Suitability column
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
    
    
   return True

def validate_table_5(table):
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
   return True

def validate_table_6(table):
    # Validate values in Suitability column
    if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"

    return True
