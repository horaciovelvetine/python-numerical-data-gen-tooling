systems_life_expectancy = [
    {
        "facilities": list(range(1, 29)), "label": "Foundation", "life_expectancy": 60
    },
    {
        "facilities": [1,2,3,4,5,6,7,8,14,15,18,21,24,25,26],
        "label": "Basement", "life_expectancy": 60
    },
    {
        "facilities": list(range(1, 29)), "label": "Superstructure", "life_expectancy": 50
    },
    {
        "facilities": list(range(1, 29)), "label": "Exterior Structure", "life_expectancy": 40
    },
    {
        "facilities": list(range(1, 29)), "label": "Roofing", "life_expectancy": 20
    },
    {
        "facilities": [f for f in range(1,29) if f not in [16,20,27]], "label": "Interior Construction", "life_expectancy": 30
    },
    {
        "facilities": [f for f in range(1,29) if f not in [16,17,20,23,27]], "label": "Stairs", "life_expectancy": 40
    },
    {
        "facilities": [], "label": "Interior Finishes", "life_expectancy": 20
    },
    {
        "facilities": [], "label": "Conveying", "life_expectancy": 10
    },
    {
        "facilities": [], "label": "Plumbing", "life_expectancy": 30
    },
    {
        "facilities": [6,11,14,19], "label": "Art", "life_expectancy": 10
    },
    {
        "facilities": [f for f in range(1,29) if f not in [12,16,17,20,23,28]], "label": "HVAC", "life_expectancy": 40
    },
    {
        "facilities": [], "label": "Fire Protection", "life_expectancy": 30
    },
    {
        "facilities": [f for f in range(1,29) if f != 12], "label": "Electric", "life_expectancy": 40
    },
    {
        "facilities": [f for f in range(1,29) if f not in [12,16,17,20,23,28]], "label": "Furnishing", "life_expectancy": 20
    },
    {
        "facilities": [f for f in range(1,29) if f != 12], "label": "Protection", "life_expectancy": 10
    },
    {
        "facilities": [2,3,4,5,6,7,8,9,11,15,19,21], "label": "Special construction", "life_expectancy": 10
    },
    {
        "facilities": [f for f in range(1,29) if f != 16], "label": "Improvements", "life_expectancy": 10
    },
    {
        "facilities": [f for f in range(1,29) if f not in [12,17]], "label": "Utilities", "life_expectancy": 30
    },
    {
        "facilities": [f for f in range(1,29) if f != 12], "label": "Distribution", "life_expectancy": 30
    },
    {
        "facilities": [f for f in range(1,29) if f != 12], "label": "Other Construction", "life_expectancy": 30
    },
    {
        "facilities": [f for f in range(1,29) if f != 12], "label": "Special construction2", "life_expectancy": 30
    }
]