import json
from typing import Union
import requests
from http import HTTPStatus
from custom_exception import CustomException
from Logger import Logger 

def upload_artifact(self, artifact_path: str, keywords: list[str]):
        url = f"https://snn-api-1080718910311.us-east1.run.app/artifacts/upload"
        print (url)
        headers = {
            "SELFNEURON-API-KEY": self.api_key,
        }

        print (artifact_path + " " + str(keywords))

        # Build the form-data structure
        with open(artifact_path, 'rb') as file:
            filename = artifact_path.split("/")[-1]
            files = {
                "files": (filename, file, "application/octet-stream"),
            }

            data = {
                "filesKeywords": json.dumps({filename: keywords}),
                "artifactText": ""
            }
            print("Request:", requests)
            response = requests.post(url=url, headers=headers, files=files, data=data)

        # Handle response
        if response.status_code == 200:
            print("Upload successful:", response.json())
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            print("Unauthorized. Wrong API key")
            raise Exception("Unauthorized. Wrong API key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            print("Operation not permitted.")
            raise Exception("Operation not permitted.")
        else:
            print("Upload failed:")
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")
        
def get_active_subscriptions():
        url = f"https://snn-api-1080718910311.us-east1.run.app/subscription/active"
        headers = {
            "SELFNEURON-API-KEY": '3OCb3RbHKlYJ6Cm3khtnX9xCw_vxIXd4AW8M3KK53I4',
             "Content-Type": "application/json",
        }
        try:
            print (url)
            response = requests.get(url=url, headers=headers)

            if response.status_code == HTTPStatus.OK:
                data = response.json()
                
                print(data)
                return data
            else:
               
                return None
        except Exception as e:
           # logger.exception("Exception while fetching active subscriptions")
            return {"error": "Failed to fetch active subscriptions", "details": str(e)}
        
def get_search_history_by_date(date: str, user_id: str = None):
        url = f"https://snn-api-1080718910311.us-east1.run.app/search/history/{date}"
        if user_id:
            url += f"?id={user_id}"

       
        headers = {
            "SELFNEURON-API-KEY": '3OCb3RbHKlYJ6Cm3khtnX9xCw_vxIXd4AW8M3KK53I4',
             "Content-Type": "application/json",
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            
            print(data)  # Print the full response
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
           # logger.error("Unauthorized. Invalid API key.")
            raise Exception("Unauthorized. Invalid API key.")
        else:
           # logger.error(f"Failed to retrieve history. Status: {response.status_code}, Response: {response.text}")
            return None
    
        
#upload_artifact(artifact_path="../tests/iPowersoft_company_profile.docx", keywords=["Documentation"])
#get_active_subscriptions()

get_search_history_by_date("All")