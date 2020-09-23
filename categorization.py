# Website Categorization using Web Shrinker
#
# Carl Pietrzak
# 9-22-2020
#
# This program uses a CSV file named 'Domain_Cat' as an input
# and outputs into a new CSV file, 'Domain_Cat_out'
# The first column in the input must contain a list of URLs
# The output file replicates the first column, then adds returned descriptors 
# to each subsequent column.

import requests, csv
from base64 import urlsafe_b64encode

csv_file_in = 'Domain_Cat.csv'
csv_file_out = 'Domain_Cat_out.csv'

# Access parameters for the Web Shrinker API
api_base_url = "https://api.webshrinker.com/categories/v3/%s"
key = "<put API key here>"
secret_key = "<put API secret key here>"

# API call
def get_categories(target_website):
    api_url = api_base_url % urlsafe_b64encode(target_website).decode('utf-8')
    response = requests.get(api_url, auth=(key, secret_key))
    status_code = response.status_code
    data = response.json()

    category_list = []

    if status_code == 200:
        # Extract category data from the JSON response
        returned_category_info = data['data'][0]['categories']
        for category in range(0, len(returned_category_info)):
            category_list.append(returned_category_info[category]['label'])

    # Return the list of categories
    # If the query status code is not '200', return an empty list
    return(category_list)


with open(csv_file_in, mode='r', newline='') as csvfile_in:
    with open(csv_file_out, mode='w', newline='') as csvfile_out:

        reader = csv.reader(csvfile_in)
        writer = csv.writer(csvfile_out)

        for row in reader:
            category_list = get_categories(str.encode(row[0]))
            row_elements = row + category_list
            writer.writerow(row_elements)
