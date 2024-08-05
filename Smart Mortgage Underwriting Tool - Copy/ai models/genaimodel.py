import openai

def generate_summary(data):
    prompt = f"Generate a summary based on the following data: {data}"
    response = openai.Completion.create(
        model = "gpt-4",
        prompt = prompt,
        max_tokens = 150
    )
    return response.choices[0].text.strip()

example_data = {
    'income': 75000,
    'assets': 200000,
    'liabilities': 50000,
    'property_value': 350000,
    'section_header': 'Income'
}
summary = generate_summary(example_data)
print(summary)
