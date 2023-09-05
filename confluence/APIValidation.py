import pandas as pd


def validate_numeric_values(column):
    return pd.to_numeric(column, errors='coerce').notna().all()

def validate_storage_table(table):
   # Validate values in Temp Storage column
   scratch_tb = table.iloc[0,0]
   longterm_tb = table.iloc[0,1]
   if not validate_numeric_values(scratch_tb):
      return False, "Temp Storage (TB) column contains non-numeric values"
   elif not validate_numeric_values(longterm_tb):
      return False, "Long-Term Storage (TB) column contains non-numeric values"
   return True

def validate_memory_table(table):
   if not validate_numeric_values(table['Amount (GB)']):
      return False, "Memory (RAM) table contains non-numeric values"
   return True

def validate_gui_table(table):
    # Validate values in Suitability column
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
   return True

def validate_research_field_table(table):
    # Validate values in Suitability column
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
   return True

def validate_table_5(table):
   if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
   return True

def validate_job_class_table(table):
    # Validate values in Suitability column
    if not table['Suitability'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"

    return True
