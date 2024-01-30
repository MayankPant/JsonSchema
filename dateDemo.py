from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

# Get user input for a date
user_input = input("Enter a date (dd/mm/yyyy): ")

# Convert user input to a datetime object
user_date = datetime.strptime(user_input, "%d/%m/%Y")

# Compare the dates
if current_datetime > user_date:
    print("The current date is later than the user input date.")
elif current_datetime < user_date:
    print("The current date is earlier than the user input date.")
else:
    print("The current date is equal to the user input date.")
