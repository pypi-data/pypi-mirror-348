from typing import Union
from selfneuron.client import SelfNeuron as SNN

base_url = 'https://snn-api-1080718910311.us-east1.run.app'
api_key = 'vFdCxMziK1Ewe52ltww5ao7NxisLti8bggrKkTaWSeY'

def test_basic_connection():
    nn = SNN(base_url=base_url, api_key=api_key)
    nn.upload_artifact("tests/iPowersoft_company_profile.docx", keywords="org profile")
    print("file list", nn.get_artifacts())

def test_pdf_upload():
    nn = SNN(base_url=base_url, api_key=api_key)
    nn.upload_artifact("tests/sreekanth_settur.pdf", keywords="profile")
    nn.get_artifacts()

def test_invalid_apikey():
    nn = SNN(base_url=base_url, api_key='edjcYa-dBgQagWQM3Edwx_0LocDKDdaqD9ERhr8EgBs123')
    nn.upload_artifact("tests/entries.csv", keywords="dummy_database")
    nn.get_artifacts()

def test_get_artifacts():
    nn = SNN(base_url=base_url, api_key=api_key)
    artifacts = nn.get_artifacts()
    print(artifacts)

def test_get_profiles():
    nn = SNN(base_url=base_url, api_key=api_key)
    profiles = nn.get_userprofile()
    print(profiles)

def test_getkeywords():
    nn = SNN(base_url=base_url, api_key=api_key)
    keywords = nn.get_keywords()
    print(keywords)

def test_search():
    nn = SNN(base_url=base_url, api_key=api_key)
    response = nn.search('ipowersoft')
    print(f"answers {response[0]}")
    print(f"recommendations {response[1]}")
    print(f"similar contents {response[2]}")

def test_recommendations():
    nn = SNN(base_url=base_url, api_key=api_key)
    recommended_questions = nn.get_recommendations()
    print(recommended_questions)

def test_enable_artifact_archieve():
    nn = SNN(base_url=base_url, api_key=api_key)
    documents = "iPowersoft_company_profile.docx"
    nn.get_artifacts()
    nn.set_artifact_archieve(documents, True)
    test_search()

def test_disable_artifact_archieve():
    nn = SNN(base_url=base_url, api_key=api_key)
    documents = "iPowersoft_company_profile.docx"
    nn.get_artifacts()
    nn.set_artifact_archieve(documents, False)
    test_search()

def test_update_user_profile():
    nn = SNN(base_url=base_url, api_key=api_key)
    nn.update_user_profile(user_name="Sreekanth Settur", agreed_terms=True)


