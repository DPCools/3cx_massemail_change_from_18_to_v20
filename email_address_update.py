import xml.etree.ElementTree as ET

def update_email_address(xml_file, output_file):
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Track modified emails to avoid duplicates
    email_tracker = {}

    # Iterate through each Extension element in the XML
    for extension in root.findall('.//Extension'):
        first_name_element = extension.find('FirstName')
        email_element = extension.find('EmailAddress')

        if first_name_element is not None and email_element is not None:
            first_name = first_name_element.text
            email = email_element.text

            # Extract the first part of the email (before the '@' symbol)
            email_prefix = email.split('@')[0]
            email_domain = email.split('@')[1]

            # Replace spaces with dots in the first name
            formatted_first_name = first_name.replace(' ', '.')

            # If the first name is not part of the email prefix, update the email
            if formatted_first_name.lower() not in email_prefix:
                new_email_prefix = f"{email_prefix}+{formatted_first_name}"

                # Check for duplicates and increment if necessary
                counter = 1
                unique_email_prefix = new_email_prefix
                while unique_email_prefix in email_tracker:
                    unique_email_prefix = f"{new_email_prefix}.{counter}"
                    counter += 1
                
                email_tracker[unique_email_prefix] = True
                new_email = f"{unique_email_prefix}@{email_domain}"
                email_element.text = new_email
                print(f"Updated EmailAddress: {new_email}")

    # Save the modified XML back to the file
    tree.write(output_file)
    print(f"Updated XML saved to {output_file}")

# Usage
update_email_address('data.xml', 'data_modified.xml')
