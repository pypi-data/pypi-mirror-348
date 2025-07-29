import json
from typing import Union
import requests
from http import HTTPStatus
from custom_exception import CustomException
from Logger import Logger

logger = Logger().get_logger()

class SelfNeuron:
    api_key = None
    base_url = None
    bearer_token = None
    artifact_mapping = {}
    
    def __init__(self, base_url:str, api_key:str, bearer_token:str):
        self.base_url = base_url
        self.api_key = api_key
        self.bearer_token = bearer_token

    

    def generate_api_key(self, key_name: str):
        url = f"{self.base_url}/api/keys/generate/{key_name}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

        response = requests.post(url=url, headers=headers)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"Generated API Key: {data}")
            return data
        else:
            logger.error(f"API Key generation failed. Status: {response.status_code}, Response: {response.text}")
            return None
    
    def list_api_keys(self):
        url = f"{self.base_url}/api/keys"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"Retrieved API Keys: {data}")
            print(data)  # You can pretty-print or structure as needed
            return data
        else:
            logger.error(f"Failed to fetch API keys. Status: {response.status_code}, Response: {response.text}")
            return None

    def delete_api_key(self, key_name):
        url = f"{self.base_url}/api/keys/{key_name}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

        response = requests.delete(url=url, headers=headers)

        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f"Successfully deleted API key: {key_name}")
            print(f"API key '{key_name}' deleted successfully.")
            return True
        else:
            logger.error(f"Failed to delete API key '{key_name}'. Status: {response.status_code}, Response: {response.text}")
            print(f"Failed to delete API key '{key_name}'.")
            return False

    def get_artifacts(self):
        if self.api_key is None:
            raise Exception("api key is not set")
        url = f"{self.base_url}/artifacts"
        headers = {
            "Connection": "keep-alive",
            "SELFNEURON-API-KEY": self.api_key
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
            
            for entry in data:
                if entry.get('artifactId') not in self.artifact_mapping:
                    self.artifact_mapping.update({entry.get('artifactId'):entry.get('artifactFileName')})
                # file_names.append(entry.get('artifactFileName'))
            logger.info(response.json())
            return self.artifact_mapping

        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")

    def upload_artifact(self, artifact:str, keywords:Union[list, str]):
        url = f"{self.base_url}/artifacts/upload"
        headers = {
            "Connection": "keep-alive",
            "Content-Type": "multipart/form-data",
            "SELFNEURON-API-KEY": self.api_key,
        }
        if isinstance(keywords, str):
            keywords = [keywords]

        data = {
            "keywords": keywords
        }
        files = {"file": open(artifact, 'rb')}
        response = requests.post(url=url, headers=headers, data=data, files=files)
        if response.status_code == 200:
            logger.info(response.json())
            self.get_artifacts() #Added to refresh the artifact mapping dict with updated artifact
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")
    
    def update_artifact_status(self, artifact_id: str):
        url = f"{self.base_url}/artifacts/{artifact_id}/true"
        headers = {
            "SELFNEURON-API-KEY": self.api_key
        }

        response = requests.post(url, headers=headers)
        print("Response:", response)
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            print("Artifact marked as true:", data)
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. Check your API key or bearer token.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("Operation not permitted.")
        else:
            raise CustomException(f"Request failed. Status: {response.status_code}, Detail: {response.text}")

    
    def generate_otp(self, email: str):
        url = f"{self.base_url}/auth/otp/generate"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        payload = {
            "email": email
        }

        response = requests.post(url=url, headers=headers, json=payload)
        
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"OTP generated response: {data}")
            
            return data
        else:
            logger.error(f"Failed to generate OTP. Status: {response.status_code}, Response: {response.text}")
            return None
        
    def validate_otp(self, email: str, code: str):
        url = f"{self.base_url}/auth/otp/validate"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        payload = {
            "email": email,
            "code": code
        }

        response = requests.post(url=url, headers=headers, json=payload)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"OTP validation response: {data}")
            return data
        else:
            logger.error(f"OTP validation failed. Status: {response.status_code}, Response: {response.text}")
            return None
    
    def get_keywords(self):
        url = f"{self.base_url}/keywords"
        headers = {
            "Connection": "keep-alive",
            # "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key,
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
        
        keywords = []
        for entry in data:
            if entry.get('isActive'):
                keywords.append(entry.get('keyword'))
        logger.info(f"keywords retrieved {keywords}")
        return keywords
    
    def get_userprofile(self):
        url = f"{self.base_url}/user/profile"
        headers = {
            "Connection": "keep-alive",
            # "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key,
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            return {'email':response.json().get('email'),
                    'name':response.json().get('name'),
                    'altEmail': response.json().get('altEmail'),
                    'device':response.json().get('device'),
                    'location':response.json().get('location')
            }
    def delete_account(self, email: str = None):
        url = f"{self.base_url}/user/profile/delete-account"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }
        payload = {
            "email": email
        }

        response = requests.delete(url=url, headers=headers, json=payload)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"Account deletion response: {data}")
            print(data)  # Full response for debug
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.error("Unauthorized. Check bearer token.")
            raise Exception("Unauthorized. Invalid bearer token.")
        else:
            logger.error(f"Failed to delete account. Status: {response.status_code}, Response: {response.text}")
            return None

    def search(self, search_str:str):
        url = f"{self.base_url}/search"
        headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept":'application/json',
            "SELFNEURON-API-KEY": self.api_key,
        }
        
        data = json.dumps({
            "text": search_str,
            "keywords": []
        }) 

        response = requests.post(url=url, headers=headers, data=data)
        if len(response.json()['data']['answers']) == 0:
            raise Exception(f"Content not searchable. Make sure, you didn't archieved the document for content {search_str}!!!")
        data = response.json()['data']
        response_data = data['answers'][0]
        recommendations = data['recommendations']
        similar_content = data['similar_vectors']
        return response_data, recommendations, similar_content

    def get_recommendations(self):
        url = f"{self.base_url}/questions/recommendations"
        headers = {
            "Connection": "keep-alive",
            "SELFNEURON-API-KEY": self.api_key,
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
            logger.info(f"recommended questions {data}")
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")


    def get_search_history_by_date(self, date: str, user_id: str = None):
        url = f"{self.base_url}/search/history/{date}"
        if user_id:
            url += f"?id={user_id}"

        headers = {
            "SELFNEURON-API-KEY": self.api_key
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"Search history for {date}: {data}")
            print(data)  # Print the full response
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.error("Unauthorized. Invalid API key.")
            raise Exception("Unauthorized. Invalid API key.")
        else:
            logger.error(f"Failed to retrieve history. Status: {response.status_code}, Response: {response.text}")
            return None
    
    def update_search_history_flags(self, history_id: str, is_archived: bool, is_bookmark: bool):
        url = f"{self.base_url}/search/history/update"
        headers = {
            "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key
        }
        payload = {
            "historyId": history_id,
            "isArchived": is_archived,
            "isBookmark": is_bookmark
        }

        response = requests.post(url=url, headers=headers, json=payload)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            logger.info(f"Search history update response: {data}")
            print(data)  # Print full response
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.error("Unauthorized. Invalid API key.")
            raise Exception("Unauthorized. Invalid API key.")
        else:
            logger.error(f"Failed to update history. Status: {response.status_code}, Response: {response.text}")
            return None

    def set_artifact_archieve(self, artifact:Union[str, list], archieve:bool=False):
        # Perform search on the artifact_id and set the archieve flag
        if isinstance(artifact, str):
            artifact = [artifact]

        for artifact_id in  artifact:
            for id, name in self.artifact_mapping.items():
                if artifact_id == name:
                    artifact_id = id
                    break
            url = f"{self.base_url}/artifacts/{artifact_id}/{archieve}"
            headers = {
                "Connection": "keep-alive",
                "SELFNEURON-API-KEY": self.api_key,
            }
            data = {}
            response = requests.post(url=url, headers=headers, data=data)
            if response.status_code == HTTPStatus.OK:
                file_name = self.artifact_mapping.get(artifact_id)
                logger.info(f"archieve Status for {file_name} is updated to {archieve}")
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                raise CustomException("Unauthorized. wrong api-key.")
            elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
                raise CustomException("operation not permitted")

    def delete_search_history(self):
            url = f"{self.base_url}/search/history/delete"
            headers = {
                "SELFNEURON-API-KEY": self.api_key
            }

            response = requests.delete(url=url, headers=headers)

            if response.status_code == HTTPStatus.NO_CONTENT:
                logger.info(f"Search history deleted successfully.")
                print("Delete successful.")
                return True
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.error("Unauthorized. Invalid API key.")
                raise Exception("Unauthorized. Invalid API key.")
            elif response.status_code == HTTPStatus.NOT_FOUND:
               
                return False
            else:
                logger.error(f"Failed to delete history. Status: {response.status_code}, Response: {response.text}")
                return None
    
    def get_active_subscriptions(self):
        url = f"{self.base_url}/subscription/active"
        headers = {
            "SELFNEURON-API-KEY": self.api_key,
             "Content-Type": "application/json",
        }
        try:
            print (url)
            response = requests.get(url=url, headers=headers)

            if response.status_code == HTTPStatus.OK:
                data = response.json()
                logger.info(f"Fetched active subscriptions: {data}")
                print(data)
                return data
            else:
                logger.error(f"Failed to fetch subscriptions. Status: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.exception("Exception while fetching active subscriptions")
            return {"error": "Failed to fetch active subscriptions", "details": str(e)}
        
    
    def get_user_billing(self):
        url = f"{self.base_url}/subscription/billing"
        headers = {
            "SELFNEURON-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
      
        try:
            print(url)
            response = requests.get(url, headers=headers)
            print (response)
            if response.status_code == HTTPStatus.OK:
                data = response.json()
                logger.info(f"Fetched billing information: {data}")
                return data
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.error("Unauthorized. Invalid API key.")
                raise Exception("Unauthorized. Invalid API key.")
            else:
                logger.error(f"Failed to fetch billing. Status: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.exception("Exception while fetching billing information")
            return {"error": "Failed to fetch billing information", "details": str(e)}
        
    def get_user_metrics(self):
        url = f"{self.base_url}/subscription/metrics"
        headers = {
            "SELFNEURON-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == HTTPStatus.OK:
                data = response.json()
                logger.info(f"Fetched user metrics: {data}")
                return data
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.error("Unauthorized. Invalid API key.")
                raise Exception("Unauthorized. Invalid API key.")
            else:
                logger.error(f"Failed to fetch user metrics. Status: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.exception("Exception while fetching user metrics")
            return {"error": "Failed to fetch user metrics", "details": str(e)}


    def update_artifact_keywords(self, artifact_id: str, keywords: list[str]):
        url = f"{self.base_url}/artifacts/keywords"
        headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key
        }
        payload = {
            "artifactId": artifact_id,
            "keywords": keywords
        }

        response = requests.put(url, json=payload, headers=headers)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            print("Keywords updated successfully:", data)
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. Wrong API key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("Operation not permitted.")
        else:
            raise CustomException(f"Request failed. Status: {response.status_code}, Detail: {response.text}")

    def update_user_profile(self, user_name:Union[None, str]=None, agreed_terms:bool=True):
        url = f"{self.base_url}/user/profile"

        data = json.dumps({
            "name": user_name
        })
        headers = {
            "Connection": "keep-alive",
            'Content-Type': 'application/json',
            "SELFNEURON-API-KEY": self.api_key,
        }

        response = requests.put(url, headers=headers, data=data)
        print (response)
        if response.status_code == HTTPStatus.OK:
            return True
