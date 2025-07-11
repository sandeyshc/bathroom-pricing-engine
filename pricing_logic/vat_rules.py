def get_vat_rate(location):
    """
    Get the VAT (Value Added Tax) rate based on location.
    
    Args:
        location (str): The city name for which to retrieve the VAT rate.
    
    Returns:
        float: The VAT rate as a decimal (e.g., 0.20 for 20%).
              Returns default rate of 0.20 if location is not found.
    """
    vat_rates = {
        'Marseille': 0.20,
        'Paris': 0.25
    }
    return vat_rates.get(location, 0.20)

def apply_vat(price, vat_rate):
    """
    Apply VAT to a given price.
    
    Args:
        price (float): The original price without VAT.
        vat_rate (float): The VAT rate as a decimal (e.g., 0.20 for 20%).
    
    Returns:
        float: The price with VAT included.
    """
    return price * (1 + vat_rate)