import requests
import json

class FullContact(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = url = "https://api.fullcontact.com/v2/person.json"
    def get(self, **kwargs):
        if 'apiKey' not in kwargs:
            kwargs['apiKey'] = self.api_key
        r = requests.get(self.url, params=kwargs)
        return json.loads(r.text)
    
    def change_keys(self,d):
        modified_response={}
        for keys in d:
            key=keys[49:]
            modified_response[key]=d[keys]
        return modified_response
    
    def post(self, email_list):
        data_dict={}
        counter=0
        chunks=[]
        person_url="https://api.fullcontact.com/v2/person.json?email="
        for i in range(len(email_list)):
            email_list[i]=person_url+email_list[i]
        
        while counter<len(email_list):
            chunks.append(email_list[counter:counter+20])
            counter+=20
            
        for request_urls in chunks:    
            post_data = json.dumps({'requests' : request_urls})
            r = requests.post(
                        'https://api.fullcontact.com/v2/batch.json',
                        params={'apiKey': self.api_key},
                        headers={'content-type': 'application/json'},
                        data=post_data).json
            json_data=json.loads(r.im_self.content)
            modified_data = self.change_keys(json_data["responses"])
            data_dict=dict(data_dict.items()+modified_data.items())
        return data_dict
