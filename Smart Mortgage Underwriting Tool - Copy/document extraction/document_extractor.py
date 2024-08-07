import os
import pandas as pd
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
from datetime import datetime

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
        "Federal income tax withheld": "f2_10[0]"
    }

    field_names_1099 = {
        "Other Income": "f2_11[0]",
        "Rents": "f2_9[0]"
    }

    field_names_1040 = {
        "Total amount from Form(s) W-2, box 1 (see instructions)": "f1_31[0]",
    }
   
    field_names_1008 = {
        "Appraised Value" : "Appraised Value",
        "Borrower Total Income" : "Borrower Total Income",
    }
    field_names_1003 = {
        "Base" : "_1b_Base[0]",
        "Overtime" : "_1b_Overtime[0]",
        "Bonus" : "_1b_Bonus[0]",
        "Commission" : "_1b_Commission[0]",
    }

    # Reverse mapping for descriptive names
    reverse_field_names_w2 = {v: k for k, v in field_names_w2.items()}
    reverse_field_names_1099 = {v: k for k, v in field_names_1099.items()}
    reverse_field_names_1040 = {v: k for k, v in field_names_1040.items()}
    reverse_field_names_1008 = {v: k for k, v in field_names_1008.items()}
    reverse_field_names_1003 = {v: k for k, v in field_names_1003.items()}

    # Determine which dictionary to use based on document text
    if 'You may file Forms W-2 and' in text:
        reverse_field_names = reverse_field_names_w2
        ignore_checkboxes = False
    elif '1099' in text:
        reverse_field_names = reverse_field_names_1099
        ignore_checkboxes = True
    elif '1040' in text: 
        reverse_field_names = reverse_field_names_1040
        ignore_checkboxes = True
    elif '1008' in text: 
        reverse_field_names = reverse_field_names_1008
        ignore_checkboxes = True
    elif '1003' in text: 
        reverse_field_names = reverse_field_names_1003
        ignore_checkboxes = True
    else:
        reverse_field_names = {}
        ignore_checkboxes = False

    extracted_info = {}
    for field_name, field_value in form_fields.items():
        # Ignore specific unknown fields (like checkboxes) for form 1099 only
        if ignore_checkboxes and (field_name.startswith("c1_") or field_name.startswith("c2_")):
            continue
        # Map the form field name to the descriptive name only if it exists
        descriptive_name = reverse_field_names.get(field_name)
        if descriptive_name:
            extracted_info[descriptive_name] = field_value

    return extracted_info

def process_pdfs_in_directory(directory_path):
    # Ensure the 'extracted_data' directory exists
    output_dir = os.path.join(directory_path, 'extracted_data')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_extracted_data = []
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            text = extract_text_from_pdf(pdf_path)
            form_fields = extract_form_fields(pdf_path)
            parsed_info = parse_information(text, form_fields)
            
            # Append parsed info with an identifier for the document
            for field, value in parsed_info.items():
                all_extracted_data.append({"Field Name": field, "Field Value": value})
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_extracted_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_path = os.path.join(output_dir, f'extracted_data_{timestamp}.csv')
    df.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")


def print_form_fields(pdf_path):
    form_fields = extract_form_fields(pdf_path)
    print("Form Fields Dictionary:")
    for field_name, field_value in form_fields.items():
        print(f"Field Name: {field_name}, Field Value: {field_value}")


# Example usage
directory_path = r"C:\Users\jay.murali\OneDrive - Coforge Limited\Documents\Smart Mortgage Underwriting Tool\document extraction\financial documents"
process_pdfs_in_directory(directory_path)






