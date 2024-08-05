from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    # Extract text using pdfminer
    text = extract_text(pdf_path)
    return text

def extract_form_fields(pdf_path):
    # Extract form fields using PyPDF2
    reader = PdfReader(pdf_path)
    form_fields = {}
    for page in reader.pages:
        if '/Annots' in page:
            for annot in page['/Annots']:
                field = annot.get_object()
                if '/T' in field and '/V' in field:
                    field_name = field['/T'].strip()
                    field_value = field['/V']
                    form_fields[field_name] = field_value
    return form_fields

def parse_information(text, form_fields):
    # Define field names dictionaries for different document types
    field_names_w2 = {
        "Employer identification number": "f2_02[0]",
        "Employer's name, address, and zip code": "f2_03[0]",
        "Employee's first name and initial": "f2_05[0]",
        "Employee's last name": "f2_06[0]",
        "Wages, tips, other compensation": "f2_09[0]",
        "Federal income tax withheld": "f2_10[0]",
        "Social Security Wages": "f2_11[0]",
        "Social Security tax withheld": "f2_12[0]",
        "Medicare wages and tips": "f2_13[0]",
        "Medicare tax withheld": "f2_14[0]"
    }

    field_names_1099 = {
        "Other Income": "f2_11[0]",
        "Rents": "f2_9[0]"
        
    }

    field_names_1040 = {
        # Add exact field names and values
    }

    field_names_1004 = {
        # Add exact field names and values
    }

    field_names_1008 = {
        # Add exact field names and values
    }

    field_names_1003 = {
        # Add exact field names and values
    }

    # Reverse mapping for descriptive names
    reverse_field_names_w2 = {v: k for k, v in field_names_w2.items()}
    reverse_field_names_1099 = {v: k for k, v in field_names_1099.items()}
    reverse_field_names_1040 = {v: k for k, v in field_names_1040.items()}
    reverse_field_names_1004 = {v: k for k, v in field_names_1004.items()}
    reverse_field_names_1008 = {v: k for k, v in field_names_1008.items()}
    reverse_field_names_1003 = {v: k for k, v in field_names_1003.items()}

    # Determine which dictionary to use based on document text
    if 'W-2' in text:
        reverse_field_names = reverse_field_names_w2
    elif '1099' in text:
        reverse_field_names = reverse_field_names_1099
    elif '1040' in text: 
        reverse_field_names = reverse_field_names_1040
    elif '1004' in text: 
        reverse_field_names = reverse_field_names_1004
    elif '1008' in text: 
        reverse_field_names = reverse_field_names_1008
    elif '1003' in text: 
        reverse_field_names = reverse_field_names_1003
    else:
        reverse_field_names = {}

    extracted_info = {}
    for field_name, field_value in form_fields.items():
        # Map the form field name to the descriptive name
        descriptive_name = reverse_field_names.get(field_name, "Unknown field")
        extracted_info[descriptive_name] = field_value
    
    return extracted_info

def extract_and_parse_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    form_fields = extract_form_fields(pdf_path)
    parsed_info = parse_information(text, form_fields)
    return parsed_info

def print_form_fields(pdf_path):
    form_fields = extract_form_fields(pdf_path)
    print("Form Fields Dictionary:")
    for field_name, field_value in form_fields.items():
        print(f"Field Name: {field_name}, Field Value: {field_value}")

# Example usage
pdf_path = r"C:\Users\jay.murali\OneDrive - Coforge Limited\Documents\Smart Mortgage Underwriting Tool\document extraction\financial documents\f1099msc.pdf"

parsed_info = extract_and_parse_pdf(pdf_path)
for section, value in parsed_info.items():
    print(f"{section}: {value}")

# To print out form fields
# print_form_fields(pdf_path)
