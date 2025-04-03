# Import modules
import csv
import logging
import time
import requests

# setting up the error_log.txt file to log all the errors with time
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# define variables
file_path = 'users.csv'
api_url = 'https://example.com/api/create_user' # need to replace with the actual url

# function to create user using a POST method
def proceed_to_user_creation(user_data):
    # print (user_data)
    try:
        # Sending a POST request to create the user in the system
        response = requests.post(api_url, data=user_data)

        if response.status_code == 201: # 201 is a assumed success code.
            print(f"User {user_data['name']} created successfully.")
        else:
            # Log the error response
            logging.error(f"Failed to create user {user_data['name']}. Status code: {response.status_code}, Response: {response.text}")
            print(f"Failed to create user {user_data['name']}. Check error_log.txt for details.")

    except requests.exceptions.RequestException as e:
        # Handle request exceptions and log
        logging.error(f"Error creating user {user_data['name']}: {str(e)}")
        print(f"Error creating user {user_data['name']}. Check error_log.txt for details.")


# function to validate the users csv file to process the user creation
def validate_users_csv_file():
    # Open the csv file to read
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        # loop through the csv file
        for row in csv_reader:
            # check if required fields are present : name,email and role
            if row['name'] and row['email'] and row['role']:
                # if valid call the function to create users
                proceed_to_user_creation(row)
                # print(row)
            else:
                logging.error(f"Missing required data for user {row['name']}. Skipping this entry.")
                print(f"Missing required data for user {row['name']}. Skipping this entry.")


# main function
if __name__ == "__main__":
    try:
        validate_users_csv_file()
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred. Check error_log.txt for details.")
