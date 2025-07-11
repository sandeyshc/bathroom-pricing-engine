# Bathroom Pricing Engine

## Overview
This project is a pricing engine for bathroom renovations. It calculates costs based on materials, labor, VAT, and profit margins to generate accurate quotes.

## How to Run the Code

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/bathroom-pricing-engine.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd bathroom-pricing-engine
    ```

3. **Install dependencies**:
    ```bash
    # If you have Conda installed
    conda create -n pricing_engine python=3.10
    conda activate pricing_engine
    pip install -r requirements.txt
    
    # If you don't have Conda
    pip install -r requirements.txt
    ```

4. **Run the pricing engine**:
    ```bash
    # To run the pricing engine and generate quotes
    python pricing_engine.py
    
    # To run the test suite
    python -m tests.test_logic
    ```

    The first command will generate a quote in JSON format.

## Output JSON Schema

The output JSON contains the following fields:

- **`tasks`**: Array of task objects with detailed pricing information:
  - `material_cost`: Cost of materials for the task
  - `labor_cost`: Labor cost calculated based on time and hourly rate
  - `estimated_time`: Estimated time to complete the task (in hours)
  - `total_price`: Total price for the task
  - `vat_rate`: Applied VAT percentage
  - `margin`: Applied profit margin

- **`total_price`**: Aggregated price for the entire renovation project

## Pricing Logic

The pricing engine uses the following calculations:

- **Material Costs**: Retrieved from the `materials.json` configuration file
- **Labor Costs**: `estimated_time × hourly_rate`
- **VAT**: Applied based on the customer's location
- **Margin**: Additional percentage added to the total task price

## Assumptions

- The hourly labor rate is fixed at $50
- A standard margin of 15% is applied to all quotes
- VAT rates vary depending on the customer's location

## Edge Cases Handling

- Unrecognized tasks default to zero cost and time estimation
- The system handles invalid input gracefully

## Dependencies

- Python 3.6+
- No additional packages required