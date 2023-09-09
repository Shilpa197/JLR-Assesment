import requests

# Define the API endpoint URL for 2023 F1 season
api_url = "http://ergast.com/api/f1/2023/constructors.json"

# Make a request to get the list of constructors in the 2023 F1 season
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    constructors = data['MRData']['ConstructorTable']['Constructors']

    # Initialize a dictionary to store the best circuit for each constructor
    best_circuits = {}

    for constructor in constructors:
        constructor_id = constructor['constructorId']
        constructor_name = constructor['name']

        # Get the circuits where the constructor has participated
        circuit_url = f"http://ergast.com/api/f1/constructors/{constructor_id}/circuits.json"
        circuit_response = requests.get(circuit_url)

        if circuit_response.status_code == 200:
            circuit_data = circuit_response.json()
            circuits = circuit_data['MRData']['CircuitTable']['Circuits']

            # Initialize a dictionary to store the number of wins at each circuit
            wins_by_circuit = {}

            for circuit in circuits:
                circuit_id = circuit['circuitId']
                circuit_name = circuit['circuitName']

                # Get the race results for this circuit and constructor
                race_url = f"http://ergast.com/api/f1/constructors/{constructor_id}/circuits/{circuit_id}/results.json"
                race_response = requests.get(race_url)

                if race_response.status_code == 200:
                    race_data = race_response.json()
                    races = race_data['MRData']['RaceTable']['Races']
                    
                    # Count the number of wins for this constructor at this circuit
                    wins = sum(1 for race in races if race['Results'][0]['position'] == '1')
                    wins_by_circuit[circuit_name] = wins

            # Find the circuit with the most wins for this constructor
            best_circuit = max(wins_by_circuit, key=wins_by_circuit.get)
            best_circuits[constructor_name] = best_circuit

    # Print the results
    for constructor, best_circuit in best_circuits.items():
        print(f"{constructor} performed best at {best_circuit}")

else:
    print(f"Error fetching data. Status code: {response.status_code}")
