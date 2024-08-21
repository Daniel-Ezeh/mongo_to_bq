import requests
import os
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime, timezone


load_dotenv()
api_url = os.environ['RANDOM_API_URL']

response = requests.get(api_url)

def get_random_user():
    
    try:
        response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)
        
        # Parse the JSON response
        user_data = response.json()
        
        # Extract relevant details
        user_details = user_data['results'][0]
        user_info = {
            "timeCreated": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z'),
            'uid': user_details['login']['uuid'],
            'name': f"{user_details['name']['first']} {user_details['name']['last']}",
            'email': user_details['email'],
            'gender': user_details['gender'],
            'address': f"{user_details['location']['street']['number']} {user_details['location']['street']['name']}",
            'city': user_details['location']['city'],
            'state': user_details['location']['state'],
            'country': user_details['location']['country'],
            'coordinates':"{" + f"latitude: {user_details['location']['coordinates']['latitude']}, longitude: {user_details['location']['coordinates']['longitude']}"+"}",
            'username': user_details['login']['username'],
            'dob': user_details['dob']['date'],
            'phone': user_details['phone']
        }
        
        # json_data = json.dumps(user_info, indent=4)
        return user_info

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
random_user = get_random_user()
pprint(random_user)