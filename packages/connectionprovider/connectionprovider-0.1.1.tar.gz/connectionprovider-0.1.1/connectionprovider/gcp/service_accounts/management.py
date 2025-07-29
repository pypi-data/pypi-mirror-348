from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth
import time

def _get_iam_service(credentials=None):
    """Builds and returns an IAM service client."""
    if not credentials:
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    return build('iam', 'v1', credentials=credentials)

def create_service_account(project_id, account_id, display_name, credentials=None):
    """Creates a GCP service account and a new key for it.

    Args:
        project_id: The ID of the GCP project.
        account_id: The ID for the new service account (e.g., 'my-sa').
        display_name: The display name for the service account.
        credentials: Optional. Custom credentials for authentication.
                     If None, Application Default Credentials (ADC) are used.

    Returns:
        A tuple (service_account_resource, service_account_key_resource) containing the created 
        service account object and the new key object. The key data is in 
        key['privateKeyData'] (base64 encoded).
        Returns (None, None) if an error occurs during service account or key creation.
    """
    service = _get_iam_service(credentials)
    name_parent = f'projects/{project_id}'
    sa_body = {
        'accountId': account_id,
        'serviceAccount': {
            'displayName': display_name
        }
    }
    
    created_sa = None
    try:
        created_sa = service.projects().serviceAccounts().create(
            name=name_parent, body=sa_body).execute()
        print(f"Successfully created service account: {created_sa.get('email')}")
    except HttpError as error:
        print(f"An API error occurred during service account creation: {error}")
        if error.resp.status == 409:
            print(f"Service account {account_id}@{project_id}.iam.gserviceaccount.com likely already exists.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred during service account creation: {e}")
        return None, None

        # If SA creation and validation were successful, 'created_sa' is populated.
    # Proceed to create a key for it.
    if created_sa:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                sa_name_full = created_sa.get('name') # e.g., projects/my-project/serviceAccounts/my-sa@my-project.iam.gserviceaccount.com
                key_body = {
                    'privateKeyType': 'TYPE_GOOGLE_CREDENTIALS_FILE', # Creates a JSON key
                    # 'keyAlgorithm': 'KEY_ALG_RSA_2048' # Optional, defaults to 2048
                }
                created_key = service.projects().serviceAccounts().keys().create(
                    name=sa_name_full, body=key_body).execute()
                print(f"Successfully created key for service account: {created_sa.get('email')}")
                print("Key ID: ", created_key.get('name'))
                print("IMPORTANT: The private key data is returned in the response. Secure it carefully.")
                return created_sa, created_key # Key created successfully, return
            except HttpError as error:
                print(f"Attempt {attempt + 1}/{max_retries}: API error during key creation: {error}")
                if attempt + 1 < max_retries:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("All retries failed for key creation after {max_retries} attempts.")
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries}: Unexpected error during key creation: {e}")
                if attempt + 1 < max_retries:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"All retries failed for key creation after {max_retries} attempts due to unexpected error.")
        # If the loop completes, all retries have failed
        return created_sa, None

def list_service_accounts(project_id, credentials=None):
    """Lists GCP service accounts in a project.

    Args:
        project_id: The ID of the GCP project.
        credentials: Optional. Custom credentials for authentication.
                     If None, Application Default Credentials (ADC) are used.

    Returns:
        A list of service account objects, or None if an error occurs.
    """
    service = _get_iam_service(credentials)
    name = f'projects/{project_id}'
    try:
        response = service.projects().serviceAccounts().list(name=name).execute()
        accounts = response.get('accounts', [])
        print(f"Found {len(accounts)} service accounts in project {project_id}.")
        # To list all SAs if there are many, pagination would be needed here.
        return accounts
    except HttpError as error:
        print(f"An API error occurred: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def delete_service_account(project_id, account_email, credentials=None):
    """Deletes a GCP service account.

    Args:
        project_id: The ID of the GCP project.
        account_email: The email address of the service account to delete.
        credentials: Optional. Custom credentials for authentication.
                     If None, Application Default Credentials (ADC) are used.

    Returns:
        True if deletion was successful (or if SA did not exist), False otherwise.
    """
    service = _get_iam_service(credentials)
    # The name for the delete operation is the full email path of the service account.
    name = f'projects/{project_id}/serviceAccounts/{account_email}'
    try:
        service.projects().serviceAccounts().delete(name=name).execute()
        print(f"Successfully deleted service account: {account_email}")
        return True
    except HttpError as error:
        if error.resp.status == 404: # Not Found
            print(f"Service account {account_email} not found. Considered deleted.")
            return True
        print(f"An API error occurred: {error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False 