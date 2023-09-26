import pandas as pd
from pandas.api.types import is_numeric_dtype

def validate_numeric_values(column):
   if len(column) == 0:
      return True
   return is_numeric_dtype(column)

def validate_storage_table(table):
   # Validate values in Temp Storage column
   columns = table.columns
   scratch_tb = table[columns[0]]
   longterm_tb = table[columns[1]]
   if not validate_numeric_values(scratch_tb):
      return False, "Temp Storage (TB) column contains non-numeric values"
   elif not validate_numeric_values(longterm_tb):
      return False, "Long-Term Storage (TB) column contains non-numeric values"
   return True, "Storage table is valid"

def validate_memory_table(table):
   if not validate_numeric_values(table['Amount (GB)']):
      return False, "Memory (RAM) table contains non-numeric values"
   return True, "Memory is valid"

def validate_suitability(table):
   # Validate values in Suitability column
   suitibalityColumn = table.columns[1]
   if not table[suitibalityColumn].empty:
      if not table[suitibalityColumn].isin([0, 1, 2]).all():
         return False, "Suitability column does not contain 0, 1, 2"
   return True, "suitability is valid"