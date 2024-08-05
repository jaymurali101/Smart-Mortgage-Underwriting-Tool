
def get_sf_connection():
    from simple_salesforce import Salesforce
    return Salesforce(
        username='your_sf_username',
        password='your_sf_password',
        security_token='your_sf_security_token',
        domain='login'  # Change to 'test' for sandbox environment
    )
