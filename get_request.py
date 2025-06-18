import requests

def fetch_user_names(url: str):
    try:
        # Send a GET request to the given URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse JSON response
        users = response.json()
        if not isinstance(users, list):
            raise ValueError("Expected a list of users in the response")

        # Extract and display user names
        print("List of user names:")
        for user in users:
            name = user.get("name")
            if name:
                print(f"- {name}")
            else:
                print("- [Name missing in user data]")

    except requests.exceptions.RequestException as req_err:
        print(f"Network or connection error: {req_err}")
    except ValueError as val_err:
        print(f"Invalid JSON structure: {val_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

# Example usage
if __name__ == "__main__":
    fetch_user_names("https://jsonplaceholder.typicode.com/users")
