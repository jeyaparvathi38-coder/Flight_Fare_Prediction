import pandas as pd
import numpy as np

def preprocess_input(data):
    """
    Transforms the raw form input dictionary into a format suitable for the Random Forest model.
    Expected feature names in exact order:
    ['Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Min', 'Arrival_Hour', 
     'Arrival_Min', 'Duration_Minutes', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo', 
     'Airline_Jet Airways', 'Airline_Jet Airways Business', 'Airline_Multiple carriers', 
     'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 'Airline_Trujet', 
     'Airline_Vistara', 'Airline_Vistara Premium economy', 'Source_Chennai', 'Source_Delhi', 
     'Source_Kolkata', 'Source_Mumbai', 'Destination_Cochin', 'Destination_Delhi', 
     'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi']
    """
    
    # Initialize all features to 0
    features = {
        'Total_Stops': int(data.get('total_stops', 0)),
        'Journey_Day': 0,
        'Journey_Month': 0,
        'Dep_Hour': 0,
        'Dep_Min': 0,
        'Arrival_Hour': 0,
        'Arrival_Min': 0,
        'Duration_Minutes': 0,
        'Airline_Air India': 0,
        'Airline_GoAir': 0,
        'Airline_IndiGo': 0,
        'Airline_Jet Airways': 0,
        'Airline_Jet Airways Business': 0,
        'Airline_Multiple carriers': 0,
        'Airline_Multiple carriers Premium economy': 0,
        'Airline_SpiceJet': 0,
        'Airline_Trujet': 0,
        'Airline_Vistara': 0,
        'Airline_Vistara Premium economy': 0,
        'Source_Chennai': 0,
        'Source_Delhi': 0,
        'Source_Kolkata': 0,
        'Source_Mumbai': 0,
        'Destination_Cochin': 0,
        'Destination_Delhi': 0,
        'Destination_Hyderabad': 0,
        'Destination_Kolkata': 0,
        'Destination_New Delhi': 0
    }

    # Date parsing
    if 'journey_date' in data:
        try:
            journey_date = pd.to_datetime(data['journey_date'], format='%Y-%m-%d')
            features['Journey_Day'] = int(journey_date.day)
            features['Journey_Month'] = int(journey_date.month)
        except:
            pass

    # Dep Time parsing
    if 'dep_time' in data:
        try:
            dep_time = pd.to_datetime(data['dep_time'], format='%H:%M')
            features['Dep_Hour'] = int(dep_time.hour)
            features['Dep_Min'] = int(dep_time.minute)
        except:
            pass

    # Arrival Time parsing
    if 'arrival_time' in data:
        try:
            arr_time = pd.to_datetime(data['arrival_time'], format='%H:%M')
            features['Arrival_Hour'] = int(arr_time.hour)
            features['Arrival_Min'] = int(arr_time.minute)
        except:
            pass

    # Duration parsing (calculating duration if possible)
    if 'dep_time' in data and 'arrival_time' in data:
        try:
            dep_h = features['Dep_Hour']
            dep_m = features['Dep_Min']
            arr_h = features['Arrival_Hour']
            arr_m = features['Arrival_Min']
            
            dep_total = dep_h * 60 + dep_m
            arr_total = arr_h * 60 + arr_m
            
            # if arrival is on next day
            if arr_total < dep_total:
                arr_total += 24 * 60
                
            features['Duration_Minutes'] = arr_total - dep_total
        except:
            pass

    # Airline
    airline = data.get('airline', '')
    airline_key = f'Airline_{airline}'
    if airline_key in features:
        features[airline_key] = 1

    # Source
    source = data.get('source', '')
    source_key = f'Source_{source}'
    if source_key in features:
        features[source_key] = 1

    # Destination
    destination = data.get('destination', '')
    destination_key = f'Destination_{destination}'
    if destination_key in features:
        features[destination_key] = 1

    # Return as an ordered list expected by the model
    # Maintain exact order:
    ordered_keys = [
        'Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Min', 'Arrival_Hour', 
        'Arrival_Min', 'Duration_Minutes', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo', 
        'Airline_Jet Airways', 'Airline_Jet Airways Business', 'Airline_Multiple carriers', 
        'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 'Airline_Trujet', 
        'Airline_Vistara', 'Airline_Vistara Premium economy', 'Source_Chennai', 'Source_Delhi', 
        'Source_Kolkata', 'Source_Mumbai', 'Destination_Cochin', 'Destination_Delhi', 
        'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi'
    ]
    
    input_vector = [features[k] for k in ordered_keys]
    
    # Needs to be a 2D array for predict()
    return np.array(input_vector).reshape(1, -1)
