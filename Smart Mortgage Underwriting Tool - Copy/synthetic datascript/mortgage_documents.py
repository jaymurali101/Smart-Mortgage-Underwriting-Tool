import pandas as pd
from faker import Faker
import random
from config import get_sf_connection  
from simple_salesforce import Salesforce
from fpdf import FPDF

sf = get_sf_connection()

class MortgageDocument:
    def __init__(self, doc_type):
        self.doc_type = doc_type
        self.data = []

    def generate_data(self): 
        raise NotImplementedError("Subclasses must implement generate_data()")

    def to_dict(self):
        return {self.doc_type: self.data}

    def save_to_pdf(self):
        """ Convert data to PDF file and save """
        if not self.data:
            print(f"No data available for {self.doc_type}")
            return 
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Data for {self.doc_type}", ln=True, align='C')

        headers = self.data[0].keys()
        for header in headers:
            pdf.cell(40, 10, txt=header, border=1)
        pdf.ln()

        for record in self.data:
            for key, value in record.items():
                pdf.cell(40, 10, txt=str(value), border=1)
            pdf.ln()

        file_name = f"{self.doc_type}_data.pdf"
        pdf.output(file_name)
        print(f"Data saved to PDF file: {file_name}")

    def upload_to_sf(self):
        """ Upload PDF to Salesforce SyntheticData object """
        if not self.data:
            print(f"No data available for {self.doc_type}")
            return

        file_path = f"{self.doc_type}_data.pdf"
        with open(file_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        sf.SyntheticData__c.create({
            'Name': f'{self.doc_type} Data',
            'ContentType': 'application/pdf',
            'Body': pdf_data
        })
        print(f"PDF file uploaded to Salesforce SyntheticData object: {file_path}")

class W2(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10): 
            self.data.append({
                "employer_name": faker.company(),
                "employer_ein": f"{random.randint(100000000, 999999999)}",  
                "employee_name": faker.name(),
                "employee_ssn": "XXX-XX-XXXX", 
                "wages": random.uniform(30000, 100000),  
                "federal_income_tax_withheld": random.uniform(1000, 5000),  
            })

class Form1099(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10): 
            self.data.append({
                "payer_name": faker.company(),
                "payer_ein": f"{random.randint(100000000, 999999999)}",
                "payee_name": faker.name(),
                "payee_ssn": "XXX-XX-XXXX",  
                "income_amount": random.uniform(10000, 50000),  
                "form_type": "1099"  
            })

class Form1040(MortgageDocument):
    def generate_data(self):
        for _ in range(10):  # Generate 10 records for demonstration
            self.data.append({
                "filing_status": random.choice(["Single", "Married Filing Jointly", "Head of Household"]),
                "total_income": random.uniform(50000, 150000),  # Sample total income range
                "federal_income_tax": random.uniform(5000, 20000),  # Sample tax range
                "form_type": "1040"  # Placeholder for specific type (e.g., 1040EZ)
            })

class Form1003(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10):  # Generate 10 records for demonstration
            self.data.append({
                "borrower_name": faker.name(),
                "borrower_ssn": "XXX-XX-XXXX",  # Placeholder for SSN (not recommended for real data)
                "borrower_dob": faker.date_of_birth(),
                "property_address": faker.address(),
                "loan_amount": random.uniform(100000, 500000),  # Sample loan amount range
                "loan_purpose": "Purchase",  # Placeholder for loan purpose (e.g., Purchase, Refinance)
                "gross_monthly_income": random.uniform(3000, 10000),  # Sample income
                "tax_benefits": random.uniform(500, 5000)  # Sample tax benefits
            })

class Form1004(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10):  # Generate 10 records for demonstration
            self.data.append({
                "property_address": faker.address(),
                "year_built": random.randint(1900, 2022),
                "appraisal_value": random.uniform(100000, 1000000),  # Sample appraisal value
                "property_type": random.choice(["Single Family", "Condo", "Multi-Family"]),
                "property_condition": random.choice(["Excellent", "Good", "Fair", "Poor"]),
                "property_use": random.choice(["Primary Residence", "Second Home", "Investment Property"]),
                "compliance_with_appraisal_standards": random.choice([True, False])
            })

class BankStatement(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10):  # Generate 10 records for demonstration
            beginning_balance = random.uniform(10000, 50000)
            deposits = sum([random.uniform(500, 5000) for _ in range(random.randint(5, 10))])  # Total deposits
            withdrawals = sum([random.uniform(100, 1000) for _ in range(random.randint(3, 8))])  # Total withdrawals
            ending_balance = beginning_balance + deposits - withdrawals
            self.data.append({
                "account_holder": faker.name(),
                "account_number": f"{random.randint(1000000000, 9999999999)}",  # Sample account number format
                "statement_period": f"{random.randint(1, 12)}/{random.randint(2023, 2024)}",  # Sample format for period
                "beginning_balance": beginning_balance,
                "deposits": deposits,
                "withdrawals": withdrawals,
                "ending_balance": ending_balance
            })

class RetirementAccount(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10):  # Generate 10 records for demonstration
            self.data.append({
                "account_holder": faker.name(),
                "account_number": f"{random.randint(1000000000, 9999999999)}",  # Sample account number format
                "account_type": random.choice(["401(k)", "IRA"]),  # Sample account types
                "balance": random.uniform(10000, 500000),  # Sample balance range
                "contributions": sum([random.uniform(500, 2000) for _ in range(random.randint(3, 6))])  # Total contributions
            })

class CreditReport(MortgageDocument):
    def generate_data(self):
        faker = Faker()
        for _ in range(10):  # Generate 10 records for demonstration
            self.data.append({
                "borrower_name": faker.name(),
                "borrower_ssn": "XXX-XX-XXXX",  # Placeholder for SSN (not recommended for real data)
                "credit_score": random.randint(600, 850),  # Sample credit score range
                "credit_lines": sum([random.uniform(5000, 20000) for _ in range(random.randint(3, 5))]),  # Total credit lines
                "payment_history": random.choice(["On Time", "30 Days Late", "60 Days Late"])  # Sample payment history
            })

# Example of generating, saving to PDF, and uploading to Salesforce
if __name__ == "__main__":
    documents = [W2("W2"), Form1099("1099"), Form1040("1040"), Form1003("1003"), Form1004("1004"), BankStatement("Bank Statement"), RetirementAccount("Retirement Account"), CreditReport("Credit Report")]

    for doc in documents:
        doc.generate_data()
        doc.save_to_pdf()  # Save data to PDF
        doc.upload_to_sf()  # Upload PDF to Salesforce
