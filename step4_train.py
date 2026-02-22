import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# 1. Load the cleaned data
df = pd.read_csv('cleaned_concrete.csv')

# 2. Define Features (X) and Target (y)
# We use the 8 ingredients + Age to predict Strength
X = df[['Cement', 'Slag', 'FlyAsh', 'Water', 'SP', 'CoarseAgg', 'FineAgg', 'Age']]
y = df['Strength']

# 3. Split data into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train the Model (Random Forest)
print("Training the AI model... this might take a few seconds.")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Check Accuracy
score = model.score(X_test, y_test)
print(f"Model Training Complete! Accuracy (R2 Score): {score:.4f}")

# 6. Save the model to a file
with open('concrete_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as 'concrete_model.pkl'.")