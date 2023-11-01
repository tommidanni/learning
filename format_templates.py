import os
import re

# Define the directory where your HTML files are located
html_directory = './templates'

# Define the regular expression pattern to match "assets/*" strings
pattern = r'assets/([^"\']+)'


# Function to replace "assets/*" strings with "{{url_for('static', filename='*')}}"
def replace_assets_with_url_for(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Use regular expressions to replace the pattern with the desired string
    modified_content = re.sub(pattern, r"{{url_for('static', filename='\1')}}", file_content)

    with open(file_path, 'w') as file:
        file.write(modified_content)

# Iterate through HTML files in the directory
for filename in os.listdir(html_directory):
    if filename.endswith('.html'):
        file_path = os.path.join(html_directory, filename)
        replace_assets_with_url_for(file_path)

print('DONE')

