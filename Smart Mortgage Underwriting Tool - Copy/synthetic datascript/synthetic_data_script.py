import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples):
    # Randomly generate base features
    wages = np.random.randint(40000, 80000, num_samples)
    federal_tax = np.random.randint(3000, 7000, num_samples)
    other_income = np.random.randint(1000, 3000, num_samples)
    rents = np.random.randint(1000, 2000, num_samples)
    total_income_w2 = np.random.randint(50000, 90000, num_samples)
    appraised_value = np.random.randint(250000, 500000, num_samples)
    borrower_total_income = np.random.randint(50000, 90000, num_samples)
    base = np.random.randint(2000, 4000, num_samples)
    overtime = np.random.randint(1000, 3000, num_samples)
    bonus = np.random.randint(500, 2000, num_samples)
    commission = np.random.randint(500, 2000, num_samples)

    # Create synthetic target variable with adjusted correlation
    mortgage_amount = (0.35 * appraised_value + 
                       0.25 * borrower_total_income + 
                       0.15 * total_income_w2 + 
                       0.10 * wages +
                       0.05 * base * overtime +  # Interaction term
                       np.random.normal(0, 8000, num_samples)).astype(int)  # Adjusted noise
    
    data = {
        "Wages_Tips_Other_Compensation": wages,
        "Federal_Income_Tax_Withheld": federal_tax,
        "Other_Income": other_income,
        "Rents": rents,
        "Total_Income_W2": total_income_w2,
        "Appraised_Value": appraised_value,
        "Borrower_Total_Income": borrower_total_income,
        "Base": base,
        "Overtime": overtime,
        "Bonus": bonus,
        "Commission": commission,
        "Mortgage_Amount": mortgage_amount
    }
    
    df = pd.DataFrame(data)
    return df


# Generate synthetic data with 1000 samples
num_samples = 1000
synthetic_data = generate_synthetic_data(num_samples)

# Save to CSV
synthetic_data.to_csv("synthetic_mortgage_data.csv", index=False)

print("Synthetic data generated and saved to 'synthetic_mortgage_data.csv'.")
