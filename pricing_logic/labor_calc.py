def calculate_labor_cost(hours, hourly_rate):
    """
    Calculate the total labor cost based on hours and hourly rate.
    
    Args:
        hours (float): Number of labor hours
        hourly_rate (float): Cost per hour of labor
    
    Returns:
        float: Total labor cost
    """
    return hours * hourly_rate

def estimate_labor_time(task, room_size=1.0):
    """
    Estimate the time needed for a bathroom renovation task based on the task type and room size.
    The base times are for a standard bathroom (room_size=1.0).
    Larger bathrooms will require proportionally more time.
    
    Args:
        task (str): The type of renovation task
        room_size (float): Room size in square meters (1.0 is standard bathroom)
    
    Returns:
        float: Estimated hours required for the task
    """
    # Base times in hours for standard bathroom size
    task_times = {
        'remove tiles': 5,
        'redo plumbing': 8,
        'replace toilet': 3,
        'install vanity': 4,
        'repaint walls': 6,
        'lay tiles': 7
    }
    
    # Get the base time and multiply by room size factor
    base_time = task_times.get(task, 0)
    return base_time * room_size