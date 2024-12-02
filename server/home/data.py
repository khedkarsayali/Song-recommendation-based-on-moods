import pandas as pd

# Path to the dataset
dataset_path = r"C:\Users\Dell\Desktop\Moodify\server\home\spotify_data\dataset.csv"

# Load the dataset
df = pd.read_csv(dataset_path, dtype={'song_name': str}, low_memory=False)

# Step 1: Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Step 2: Drop unwanted columns
df = df.drop(columns=['song_name', 'unnamed: 0'], errors='ignore')

# Step 3: Check and handle missing values
missing_values = df.isnull().sum()
print("Missing values per column:")
print(missing_values)

# Drop columns with more than 50% missing values
threshold = 0.5 * len(df)
df = df.dropna(axis=1, thresh=threshold)

# Fill remaining missing values with appropriate strategies
# Example: Fill numeric columns with the median and categorical columns with the mode
for column in df.columns:
    if df[column].dtype in ['float64', 'int64']:
        df[column].fillna(df[column].median(), inplace=True)
    elif df[column].dtype == 'object':
        df[column].fillna(df[column].mode()[0], inplace=True)

# Step 4: Remove duplicates
df = df.drop_duplicates()

# Step 5: Ensure correct data types
df['duration_ms'] = pd.to_numeric(df['duration_ms'], errors='coerce')  # Convert duration to numeric
df['time_signature'] = pd.to_numeric(df['time_signature'], errors='coerce')

# Step 6: Handle outliers (optional)
# Example: Remove rows where 'duration_ms' is beyond 1.5*IQR
Q1 = df['duration_ms'].quantile(0.25)
Q3 = df['duration_ms'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['duration_ms'] >= lower_bound) & (df['duration_ms'] <= upper_bound)]

# Step 7: Save the cleaned data
cleaned_dataset_path = r"C:\Users\Dell\Desktop\Moodify\server\home\spotify_data\cleaned_dataset.csv"
df.to_csv(cleaned_dataset_path, index=False)

print("Cleaned dataset saved to:", cleaned_dataset_path)
print("Cleaned Dataset Preview:")
print(df.head())
