import csv
import json
import os

def load_resume_data(filename):
    """Load resume data from a given JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def find_file_section(csv_filename, input_filename):
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if row and row[0] == input_filename:
                return i
    return None

def read_csv_as_list(csv_filename):
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def write_list_to_csv(csv_filename, rows):
    """Write a list of rows back into the CSV file."""
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def process_resume_data(input_filename, output_filename):
    resume_data = load_resume_data(input_filename)
    if os.path.exists(output_filename):
        # Check if the file section exists
        section_index = find_file_section(output_filename, input_filename)
        rows = read_csv_as_list(output_filename)
        
        # Prepare new data
        new_data = prepare_resume_data(resume_data, input_filename)
        
        # Replace old data if new data is different; otherwise, do nothing.
        if section_index is not None:
            # Check if the context has changed
            if rows[section_index + 1:section_index + 1 + len(new_data)] != new_data:
                # Update the section with new data
                rows[section_index:section_index + len(new_data)] = new_data
                write_list_to_csv(output_filename, rows)
            # If the context is the same, do nothing
        else:
            # Append new data
            rows.extend(new_data)
            write_list_to_csv(output_filename, rows)
    else:
        # File doesn't exist, write new data
        new_data = prepare_resume_data(resume_data, input_filename)
        write_list_to_csv(output_filename, new_data)

def prepare_resume_data(resume_data, input_filename):
    headers = ["Company Name", "Job Title", "Start Date", "End Date", "Description"]
    # Prepare initial data structure with headers, excluding "Skills" for special handling
    prepared_data = [[input_filename]]  # First row with file name
    for header in headers:
        prepared_data.append([header])  # Headers in the first column

    # Fill the content for each job
    for work in resume_data['work_output']:
        prepared_data[1].append(work.get('company_name', ''))
        prepared_data[2].append(work.get('job_title', ''))
        prepared_data[3].append(work.get('start_date', ''))
        prepared_data[4].append(work.get('end_date', ''))
        prepared_data[5].append(work.get('description', ''))

    # Add skills; each skill in its own cell
    skills_row = ['Skills'] + resume_data.get('skills', [])
    prepared_data.append(skills_row)

    return prepared_data


# Example usage
if __name__ == '__main__':
    input_filename = 'resume1.txt'  # Update this path
    output_filename = 'extracted_info.csv'  # Update this path
   
    process_resume_data(input_filename, output_filename)