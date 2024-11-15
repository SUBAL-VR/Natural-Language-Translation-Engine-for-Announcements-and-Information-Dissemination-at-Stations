import re

def load_train_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    train_data = {}
    for line in lines:
        details = line.strip().split(';')
        if len(details) >= 5:
            train_data[details[0]] = {
                'destination': details[1],
                'arrival': details[2],
                'departure': details[3],
                'duration': details[4],
                'status': details[5] if len(details) > 5 else 'N/A'
            }
    return train_data

def find_train_info(train_data, query):
    # Simple keyword matching for the question
    query = query.lower()
    for train_name, details in train_data.items():
        if train_name.lower() in query or details['destination'].lower() in query:
            return (f"Train: {train_name}, Destination: {details['destination']}, "
                    f"Arrival: {details['arrival']}, Departure: {details['departure']}, "
                    f"Duration: {details['duration']}, Status: {details['status']}")
    return "Sorry, I couldn't find the train details you asked for."

def main():
    train_data = load_train_data('C:/Users/SUBAL V R/Documents/VsCode/voice-translation/final_3/trains.txt')
    
    # Example question
    question = input("Please enter your question about train details: ")
    answer = find_train_info(train_data, question)
    print(answer)


if __name__ == "__main__":
    main()
