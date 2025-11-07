# CIS-117 Lab3
# Erika Hughes
# Collaboration description: This module reads a CSV file containing country information and splits the data into multiple new CSV files, one for each unique geographical region. It only keeps the country name and region fields in the output files and includes robust exception handling for file access errors.
import csv
import os
import collections

# Define the input and output settings
INPUT_FILENAME = 'country_full.csv'
OUTPUT_DIR = 'regions_output' # Directory to store the split files
COUNTRY_FIELD = 'name' # Assuming the column header for country name
REGION_FIELD = 'region'       # Assuming the column header for region

def split_csv_by_region(input_file, output_directory, country_key, region_key):
    """
    Reads a CSV file, groups rows by region, and writes separate CSV files
    for each region containing only the country name and region.
    """
    # 1. Attempt to create the output directory
    try:
        os.makedirs(output_directory, exist_ok=True)
        print(f"Output directory '{output_directory}' ensured.")
    except OSError as e:
        # Catch errors if directory creation fails for reasons other than existence
        print(f"Error creating output directory '{output_directory}': {e}")
        return

    # 2. Attempt to read the input CSV file
    countries_by_region = collections.defaultdict(list)
    try:
        # Use 'with open' for safe file handling, 'r' for read mode
        # 'newline=' is crucial for cross-platform CSV handling
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            # Check if the required fields exist
            if country_key not in fieldnames or region_key not in fieldnames:
                print(f"Error: Required fields '{country_key}' or '{region_key}' not found in the CSV header.")
                return

            # Group the rows by region
            for row in reader:
                region = row.get(region_key)
                if region: # Only process rows that have a region defined
                    # Store only the required fields
                    countries_by_region[region].append({
                        country_key: row.get(country_key),
                        region_key: region
                    })

    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file '{input_file}'.")
        return
    except IOError as e:
        print(f"An I/O error occurred while reading the file '{input_file}': {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during file reading: {e}")
        return

    # 3. Write the split data to separate files
    output_fieldnames = [country_key, region_key]
    if not countries_by_region:
        print("No data was successfully read or grouped by region.")
        return

    for region, country_list in countries_by_region.items():
        # Clean the region name to be a valid filename (e.g., replace spaces with underscores)
        safe_region_name = region.replace(' ', '_').replace('/', '-').replace('\\', '-').strip()
        output_filename = os.path.join(output_directory, f"{safe_region_name}.csv")

        try:
            # Use 'w' for write mode, 'newline=' for CSV, 'utf-8' encoding
            with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
                writer.writeheader()
                writer.writerows(country_list)
            print(f"Successfully created: {output_filename}")

        except PermissionError:
            print(f"Error: Permission denied when trying to write to '{output_filename}'.")
        except IOError as e:
            print(f"An I/O error occurred while writing to the file '{output_filename}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file writing to '{output_filename}': {e}")

# Run the function
if __name__ == "__main__":
    split_csv_by_region(INPUT_FILENAME, OUTPUT_DIR, COUNTRY_FIELD, REGION_FIELD)