import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
print("Loading data...")
df = pd.read_csv('cleaned_concrete.csv')

# 1. Create Heatmap
print("Generating Heatmap... Please wait.")
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show() # This should pause the script until you close the window

# 2. Create Scatter Plot
print("Generating Scatter Plot...")
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Cement', y='Strength', data=df)
plt.title("Cement vs Strength")
plt.show() # This will open after you close the first window

print("Analysis complete.")