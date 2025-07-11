from transformers import pipeline
import re
import json
from pricing_logic.material_db import get_material_cost
from pricing_logic.labor_calc import calculate_labor_cost, estimate_labor_time
from pricing_logic.vat_rules import get_vat_rate, apply_vat


def parse_transcript_with_model(transcript):
    """
    Analyzes client transcript to identify renovation tasks and room size using NLP.
    
    Args:
        transcript (str): The client conversation text to analyze
        
    Returns:
        tuple: (list of detected tasks, room size in square meters)
    """
    # Load a more robust model for zero-shot classification
    # Use a more powerful model for task extraction
    nlp_model = pipeline("text-classification", model="facebook/bart-large-mnli")
    
    # Comprehensive list of possible bathroom renovation tasks
    possible_tasks = [
        "remove tiles", "redo plumbing", "replace toilet", "install toilet",
        "install vanity", "install sink", "repaint walls", "lay tiles",
        "install shower", "replace bathtub", "install bathtub", "waterproofing",
        "electrical work", "ventilation", "install lighting", "grout work",
        "caulking", "install mirror", "install cabinets", "demo work"
    ]
    
    tasks = []
    # Check each task individually with specific context
    for task in possible_tasks:
        hypothesis = f"The client wants to {task}"
        result = nlp_model(f"premise: {transcript} hypothesis: {hypothesis}")
        
        # If model is confident this task is mentioned (ENTAILMENT with high score)
        if result[0]['label'] == 'entailment' and result[0]['score'] > 0.5:
            tasks.append(task)
    
    # Fallback for common tasks using basic keyword matching if no tasks found
    if not tasks:
        for task in possible_tasks:
            if task.replace(" ", "").lower() in transcript.replace(" ", "").lower():
                tasks.append(task)
    

    # Use regex to extract room size
    room_size_match = re.search(r'(\d+\.?\d*)m²', transcript)
    room_size = float(room_size_match.group(1)) if room_size_match else None

    # Alternatively, use a language model to interpret room size
    if room_size is None:
        room_size = extract_room_size_with_llm(transcript)

    return tasks, room_size


def extract_room_size_with_llm(transcript):
    """
    Uses a question-answering model to extract bathroom size when regex fails.
    
    Args:
        transcript (str): The client conversation text to analyze
        
    Returns:
        float: Bathroom size in square meters, defaults to 5.0 if extraction fails
    """
    # Initialize the LLM pipeline directly for question answering
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    
    # Directly ask the model to extract the room size
    question = "What is the bathroom size in square meters?"
    result = qa_pipeline(question=question, context=transcript)
    
    # Try to parse the extracted answer into a number
    try:
        # Clean the answer and extract just the number
        answer = result['answer'].strip()
        size_match = re.search(r'(\d+\.?\d*)', answer)
        if size_match:
            return float(size_match.group(1))
    except:
        pass
    
    # If extraction fails, return a default size
    return 5.0  # Default fallback size


def generate_quote(transcript):
    """
    Generates a detailed price quote based on client transcript.
    
    Analyzes the transcript, identifies tasks, calculates material and labor costs,
    applies margins and VAT to produce a complete renovation quote.
    
    Args:
        transcript (str): The client conversation text
        
    Returns:
        dict: Complete quote with task breakdown and total price
    """
    tasks, room_size = parse_transcript_with_model(transcript)
    location = 'Marseille'
    hourly_rate = 50  # Example hourly rate
    margin = 0.15  # Example margin

    quote = {'tasks': [], 'room_size': room_size}
    total_price = 0

    for task in tasks:
        material_cost = get_material_cost(task)
        labor_time = estimate_labor_time(task) * (room_size / 4)  # Adjust time based on room size
        labor_cost = calculate_labor_cost(labor_time, hourly_rate)
        task_price = material_cost + labor_cost
        task_price_with_margin = task_price * (1 + margin)
        vat_rate = get_vat_rate(location)
        final_price = apply_vat(task_price_with_margin, vat_rate)

        quote['tasks'].append({
            'task': task,
            'material_cost': material_cost,
            'labor_cost': labor_cost,
            'estimated_time': labor_time,
            'total_price': final_price,
            'vat_rate': vat_rate,
            'margin': margin
        })

        total_price += final_price

    quote['total_price'] = total_price
    return quote


def main():
    """
    Main entry point of the program.
    
    Gets user input for client transcript, generates a quote,
    and writes the result to a JSON file.
    
    Raises:
        ValueError: If the transcript provided is empty
    """
    transcript = input("Enter client transcript: ")
    if not transcript.strip():
        raise ValueError("Error: Transcript cannot be empty. Please provide client details.")
    
    quote = generate_quote(transcript)
    with open('output/sample_quote.json', 'w') as file:
        json.dump(quote, file, indent=4)
    print("Output Written to file successfully.")


if __name__ == '__main__':
    main()