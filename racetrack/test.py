import re

# Define a string with multiple spaces
my_string = "Hello   world  this    is   a   string  "

# Split the string by spaces using regular expression
split_string = re.split(r'\s+', my_string)

# Filter out empty strings
split_string = [word for word in split_string if word]

# Print the result
print(split_string)

