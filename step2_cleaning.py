import pandas as pd  # 'pandas' is like Excel for Python

# 1. LOAD DATA
# We read your CSV file into a 'DataFrame' (df)
df = pd.read_csv('concrete_data.csv')

# 2. RENAME COLUMNS
# Those long names in your file are hard to type. Let's simplify them.
df.columns = ['Cement', 'Slag', 'FlyAsh', 'Water', 'SP', 'CoarseAgg', 'FineAgg', 'Age', 'Strength']

print("--- Data Loaded ---")
print(df.head()) # Shows the first 5 rows to confirm it's working

# 3. CLEANING: REMOVE EMPTY CELLS
# If any cell is blank, the AI will crash. We remove those rows.
df = df.dropna()

# 4. CLEANING: REMOVE DUPLICATES
# Removes identical test results that might be mistakes.
df = df.drop_duplicates()

# 5. CIVIL ENGINEERING CHECK: W/C RATIO
# We know W/C ratio shouldn't be too high or too low. 
# Let's create a W/C ratio column to help the AI.
df['WC_Ratio'] = df['Water'] / df['Cement']

# 6. SAVE CLEANED DATA
# This creates a new, perfect CSV file for the next step.
df.to_csv('cleaned_concrete.csv', index=False)

print("\n--- Cleaning Complete! ---")
print(f"Final number of rows: {len(df)}")
print("New file saved as: cleaned_concrete.csv")