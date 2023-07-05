import argparse
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Setup argument parser
parser = argparse.ArgumentParser(description='Organization transformation block')
parser.add_argument('--in-directory', type=str, required=True,
                    help="Input directory containing the csv files")
parser.add_argument('--out-directory', type=str, required=True,
                    help="Output directory to store the results")

# Parse the known arguments
args, unknown = parser.parse_known_args()

# Verify that the input directory exists
if not os.path.exists(args.in_directory):
    print('--in-directory argument', args.in_directory, 'does not exist', flush=True)
    exit(1)

# Create the output directory if it does not exist
if not os.path.exists(args.out_directory):
    os.makedirs(args.out_directory)

# Construct file paths for the input CSV files
eeg_path = os.path.join(args.in_directory, 'EEG_data.csv')
info_path = os.path.join(args.in_directory, 'demographic_info.csv')

# Load data from the CSV files
eeg_df = pd.read_csv(eeg_path)
info_df = pd.read_csv(info_path)

# Rename column for easier merging
info_df.rename(columns={'subject ID': 'SubjectID'}, inplace=True)

# Merge dataframes on 'SubjectID'
data = info_df.merge(eeg_df, on='SubjectID')

# Drop unnecessary columns
data = data.drop(['VideoID', 'predefinedlabel'], axis=1)

# Standardize column names
data.rename(columns={' age': 'Age', ' ethnicity': 'Ethnicity', ' gender': 'Gender', 'user-definedlabeln': 'Label'}, inplace=True)
# Convert 'Label' column to integer
data['Label'] = data['Label'].astype(int)

# Convert 'Gender' column to binary where 'M' is 1 and 'F' is 0
data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'M' else 0)

# Create dummy variables for 'Ethnicity'
ethnicity_dummies = pd.get_dummies(data['Ethnicity'], dtype=int)
data = pd.concat([data, ethnicity_dummies], axis=1)
data = data.drop('Ethnicity', axis=1)

# Separate features from target variable
features = data.drop('Label', axis=1).copy()
y = data['Label'].copy()

# Standardize the features
scaler = StandardScaler()
X = scaler.fit_transform(features)

data.rename(columns={'Label': 'Output'}, inplace=True)

# Save the resulting dataframe to a CSV file in the output directory
output_path = os.path.join(args.out_directory, 'eeg_confusion.csv')
data.to_csv(output_path, index=False)
