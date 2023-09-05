import os
import argparse
import csv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_classif


def save_row_as_csv(row_data, filename):

    with open(filename, 'w', newline='') as output_csvfile:
        csvwriter = csv.writer(output_csvfile)

        # Write the header and row data
        csvwriter.writerow(row_data.index)  # Write the headers as the first row
        csvwriter.writerow(row_data.values)  # Write the row data as the second row


def iterate_csv_and_create_new_with_headers(input_file, output_directory):
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the original CSV file
    with open(input_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # Get the header row

        # Initialize a counter for the sequence number
        sequence_number = 1

        for row in csvreader:
            # Convert the row data to a pandas Series with appropriate column names
            row_data = pd.Series(row, index=headers)

            # Save the row data as a new CSV file
            save_row_as_csv(row_data, output_directory, sequence_number)
            sequence_number += 1


if __name__ == "__main__":
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
    df = pd.read_csv(eeg_path)
    data = pd.read_csv(info_path)

    # Merging the datasets on Subject-ID
    data = data.rename(
        columns={'subject ID': 'SubjectID', ' gender': 'gender', ' age': 'age', ' ethnicity': 'ethnicity'})
    df = df.merge(data, how='inner', on='SubjectID')

    # Converting the Categorical columns to numerical ones
    df['gender'] = df['gender'].replace({'M': 1, 'F': 0})
    df['ethnicity'] = df['ethnicity'].replace({'Han Chinese': 0, 'Bengali': 1, 'English': 2})

    # Separating-out feature-set and `Target-column`
    # Mutual-info gives the score to each **Feature** which describes its *Relationship* with `Target` variable
    y = df['user-definedlabeln']
    mi_score = mutual_info_classif(df.drop('user-definedlabeln', axis=1), df['user-definedlabeln'])
    mi_score = pd.Series(mi_score, index=df.drop('user-definedlabeln', axis=1).columns)
    mi_score = (mi_score * 100).sort_values(ascending=False)

    # Selecting top-14 features
    # top_features = mi_score.head(14).index.tolist()
    top_features = ["VideoID", "Alpha2", "Delta", "Gamma1", "Theta", "Beta1", "Alpha1", "Attention", "Gamma2", "Beta2",
                    "SubjectID", "Mediation", "Raw", "ethnicity"]
    print(top_features)

    if 'predefinedlabel' in top_features:
        top_features.remove('predefinedlabel')

    df = df[top_features]

    # Scaling our *Feature*-set
    df[top_features] = StandardScaler().fit_transform(df[top_features])

    df['user-definedlabeln'] = y

    # # Save each row of the resulting dataframe as a new CSV file in the output directory
    # for _, row in df.iterrows():
    #     save_row_as_csv(row, args.out_directory, _ + 1)  # Add 1 to the index to start sequence from 1
    # Save each row of the resulting dataframe as a new CSV file in the output directory

    for idx, row in df.iterrows():
        filename_prefix = f"{int(row['user-definedlabeln'])}."  # Add a dot after the value

        # Create a new CSV file for each row
        filename = os.path.join(args.out_directory, filename_prefix + str(idx + 1)+".csv")

        save_row_as_csv(row, filename)  # Add 1 to the index to start sequence from 1