from app.calculations import calculate_heating
from app.models import SpaceHeatingModel

def run_heating_analysis():
    properties = [
        {"area": 150, "insulation_level": "high", "average_temperature": 20, "heating_type": "gas"},
        {"area": 100, "insulation_level": "medium", "average_temperature": 18, "heating_type": "electric"},
        {"area": 200, "insulation_level": "low", "average_temperature": 15, "heating_type": "oil"}
    ]

    results = []
    for prop in properties:
        model = SpaceHeatingModel(**prop)
        result = calculate_heating(model)
        results.append(result)

    for result in results:
        print(result)

if __name__ == "__main__":
    run_heating_analysis()
