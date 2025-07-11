import json

def load_materials():
    """
    Load materials data from the JSON file.
    
    Returns:
        dict: A dictionary containing materials data.
    """
    with open('data/materials.json', 'r') as file:
        return json.load(file)

def get_material_cost(material_name):
    """
    Get the cost of a specific material by name.
    
    Args:
        material_name (str): The name of the material to look up.
        
    Returns:
        float: The cost of the material, or 0 if the material is not found.
    """
    materials = load_materials()
    return materials.get(material_name, {}).get('cost', 0)