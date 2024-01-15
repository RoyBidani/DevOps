import csv

# Function to calculate average
def calculate_average(data):
    return sum(data) / len(data) if data else 0

# Open the CSV file
with open('corona.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Read the header row
    header = next(reader)

    # Create empty lists to store the data
    vaccinated_ages = []
    unvaccinated_ages = []
    hospitalization_lengths = []

    # Read each row of data
    for row in reader:
        # Extract the data from each column
        age = int(row[1])
        vaccinated = row[6]

        # Append age to respective list based on vaccination status
        if vaccinated == 'Y':
            vaccinated_ages.append(age)
        else:
            unvaccinated_ages.append(age)

        # Extract hospitalization length
        length_of_hospitalization_value = int(row[4])
        hospitalization_lengths.append(length_of_hospitalization_value)

    # Print min and max age of vaccinated and unvaccinated patients
    print("Vaccinated:")
    if vaccinated_ages:
        print("Minimum age:", min(vaccinated_ages))
        print("Maximum age:", max(vaccinated_ages))
    else:
        print("No vaccinated patients found.")

    print("\nUnvaccinated:")
    if unvaccinated_ages:
        print("Minimum age:", min(unvaccinated_ages))
        print("Maximum age:", max(unvaccinated_ages))
    else:
        print("No unvaccinated patients found.")

    # Calculate and print average length of hospitalization
    avg_hospitalization_length = calculate_average(hospitalization_lengths)
    print("\nAverage length of hospitalization:", avg_hospitalization_length)

# Filter function to create a new file with requested information
def filter_data(file_path, filter_data_list):
    # Open the CSV file
    with open('corona.csv', 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Read the header row
        header = next(reader)

        # Get the indices of the requested data columns
        indices = [header.index(item) for item in filter_data_list]

        # Create a new CSV file to store the filtered data
        with open(f'filtered_data{filter_data_list}.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(filter_data_list)  # Write the header row

            # Iterate over the data rows
            for row in reader:
                # Extract the requested data based on indices
                filtered_data = [row[index] for index in indices]

                # Write the filtered data to the new file
                writer.writerow(filtered_data)

# Prompt the user for the desired data to filter
data_to_filter = input("\nEnter the data you want to filter (comma-separated): ").split(',')

# Call the filter function to create a new file with the requested information
filter_data('corona.csv', data_to_filter)
print(f"Filtered data file created: filtered_data{data_to_filter}.csv")
