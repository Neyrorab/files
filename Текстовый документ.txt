import requests
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException
from requests.exceptions import RequestException
import os


def fetch_user_data(url):
    """Fetch user data from the given API endpoint."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("Expected a list of user objects.")
        return data
    except RequestException as e:
        print(f"[ERROR] Failed to fetch data from API: {e}")
    except ValueError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error during data fetch: {e}")
    return None


def extract_user_names(users):
    """Extract user names from the list of user dictionaries."""
    try:
        return [user.get("name", "Unnamed User") for user in users]
    except Exception as e:
        print(f"[ERROR] Failed to extract user names: {e}")
        return []


def export_to_excel(names, filename):
    """Export the list of names to an Excel file."""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(["User Names"])  # Header

        for name in names:
            ws.append([name])

        wb.save(filename)
        print(f"[SUCCESS] User names exported to '{filename}'")
    except PermissionError:
        print(f"[ERROR] Permission denied: Unable to write to '{filename}'")
    except InvalidFileException as e:
        print(f"[ERROR] Invalid Excel file: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to save Excel file: {e}")


def main():
    url = "https://jsonplaceholder.typicode.com/users"
    output_file = "users.xlsx"

    print("[INFO] Fetching user data...")
    users = fetch_user_data(url)
    if users is None:
        return

    print("[INFO] Extracting user names...")
    names = extract_user_names(users)
    if not names:
        print("[ERROR] No names to export.")
        return

    print("[INFO] Exporting to Excel...")
    export_to_excel(names, output_file)


if __name__ == "__main__":
    main()
