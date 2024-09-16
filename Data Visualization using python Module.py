import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to list all CSV and Excel files in the folder
def list_files_in_directory():
    files = [f for f in os.listdir() if f.endswith('.csv') or f.endswith('.xlsx')]
    return files

# Function to load the file based on the user selection
def load_file(file_name):
    if file_name.endswith('.csv'):
        return pd.read_csv(file_name)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(file_name)

# List available files
files = list_files_in_directory()

# Check if there are any files
if len(files) == 0:
    print("No CSV or Excel files found in the current directory.")
else:
    # Show the files to the user
    print("Available files:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")

    # Ask the user to choose a file by entering the number
    file_choice = int(input(f"Enter the number of the file you want to load (1-{len(files)}): "))
    selected_file = files[file_choice - 1]

    # Load the selected file
    Data = load_file(selected_file)
    print(f"\nFile '{selected_file}' loaded successfully.")
    
    # Show the first few rows of the dataset
    print("\nFirst few rows of the dataset:")
    print(Data.head())
    
    # Show dataset info
    print("\nBasic information about the dataset:")
    print(Data.info())

    # Show column names
    print("\nColumns in the dataset:")
    print(Data.columns.tolist())

    # Ask the user to select two columns for visualization
    print("\nPlease select valid column names from the list above.")
    x_column = input("Enter the column name for the X-axis : ").strip()
    y_column = input("Enter the column name for the Y-axis : ").strip()

    # Check if the selected columns exist
    if x_column not in Data.columns:
        raise KeyError(f"Column '{x_column}' does not exist. Please check the available columns.")
    if y_column not in Data.columns:
        raise KeyError(f"Column '{y_column}' does not exist. Please check the available columns.")

    # Data Cleaning
    Data.dropna(inplace=True)

    # Check if selected columns are numeric
    if pd.api.types.is_numeric_dtype(Data[y_column]):
        Data[y_column].fillna(Data[y_column].mean(), inplace=True)
    else:
        print(f"Warning: {y_column} contains non-numeric data, skipping fillna() for this column.")

    Data.drop_duplicates(inplace=True)

    # Ask the user to choose a plot type
    print("\nAvailable plot types:")
    print("1. Line Plot")
    print("2. Scatter Plot")
    print("3. Histogram")
    print("4. Bar Plot")
    print("5. Box Plot")
    plot_type = input("Enter the number of the plot type you want to create (1-5): ")

    # Creating the Plot based on user choice
    plt.figure(figsize=(10, 6))
    
    if plot_type == '1':
        plt.plot(Data[x_column], Data[y_column])
        plt.title('Line Plot')
    elif plot_type == '2':
        #plt.scatter(Data[x_column], Data[y_column])
        plt.scatter(Data[x_column].astype(int), Data[y_column])
        plt.title('Scatter Plot')
    elif plot_type == '3':
        plt.hist(Data[y_column], bins=30)
        plt.title('Histogram')
        plt.xlabel(y_column)
    elif plot_type == '4':
        plt.bar(Data[x_column], Data[y_column])
        plt.title('Bar Plot')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
    elif plot_type == '5':
        Data.boxplot(column=y_column, by=x_column)
        plt.title('Box Plot')
        plt.suptitle('')
    else:
        print("Invalid plot type selected.")
    
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.show()

# Ask the user to input the filename for the cleaned data file
cleaned_data_filename = input("Enter the filename for the cleaned data (without extension): ")
plot_filename = input("Enter the filename for the plot (without extension): ")

# Save the cleaned data as a CSV file using the provided filename
Data.to_csv(f'{cleaned_data_filename}.csv', index=False)

# Save the plot using the provided filename
plt.savefig(f'{plot_filename}.jpg')

# Notify the user that the files have been saved
print(f"\nCleaned data saved as '{cleaned_data_filename}.csv' and plot saved as '{plot_filename}.jpg'.")

