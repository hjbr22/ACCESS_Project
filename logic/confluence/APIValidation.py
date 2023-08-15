import pandas as pd



def validate_numeric_values(column):
    return pd.to_numeric(column, errors='coerce').notna().all()

def validate_table_1(table):
    # Validate values in Temp Storage column
   if not validate_numeric_values(table['Temp Storage (TB)']):
      return False, "Temp Storage (TB) column contains non-numeric values"
   elif not validate_numeric_values(table['Long-Term Storage (TB)']):
      return False, "Long-Term Storage (TB) column contains non-numeric values"
   elif not validate_numeric_values(table['Memory (RAM) (GB)']):
      return False, "Memory (RAM) (GB) column contains non-numeric values"
    
   return True

def validate_table_2(table):
    # Validate values in Suitability column
   if not table['Suitability How well does your system support this functionality?0 - not supported1 - supported but not well suited2- well suited'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
    
    
   return True

def validate_table_3(table):
    # Validate values in Suitability column
   if not table['Suitability How well suited is your system for this field of research? 0-can be used for this field but not recommended1-well suited2-specialized for this field of research'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
    
    
   return True

def validate_table_4(table):
    if not table['Suitability How well suited is your system for this class of Job? 0-can perform this class of job but not recommended1-well suited2-specialized for this class of job'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"

def validate_table_5(table):
    # Validate values in Suitability column
    if not table['Suitability How well suited is your system for this package/library?0-Package available but not recommended for use1-well suited2-system is specilized for this type of package/library'].isin([0, 1, 2]).all():
      return False, "Suitability column does not contain 0, 1, 2"
    elif not table['CPU/GPU Is this package for CPU or GPU?0-CPU only1-GPU only2-Both CPU and GPU'].isin([0, 1, 2]).all():
        return False, "CPU/GPU column does not contain 0, 1, 2"
    
    
    return True
