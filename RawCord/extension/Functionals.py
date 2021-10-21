import requests, json

BASE = "https://discord.com/api/v9"
CHANNEL_TYPES = {"GUILD_TEXT":0,"DM":1,"GUILD_VOICE":2,"GROUP_DM":3,"GUILD_CATEGORY":4,"GUILD_NEWS":5,"GUILD_STORE":6,"GUILD_NEWS_THREAD":10,"GUILD_PUBLIC_THREAD":11,"GUILD_PRIVATE_THREAD":12,"GUILD_STAGE_VOICE":13}

class OptionalKwargs():
    def __init__(self,kwargs):
        self.dictionary = {i:kwargs[i] for i in kwargs if kwargs[i]!=None}

    def __getitem__(self,key)->str:
        if key in self.dictionary.keys():
            return self.dictionary[key]
        return None

class InvalidArguments(Exception):
  	pass

class RateLimit(Exception):
    pass

class APIError(Exception):
    pass

def boolean(string):
    string = str(string)
    if string.lower()=="false":
        return False
    elif string.lower()=="true":
        return True
    else:
        return None

def debrief_request(r,inst,json=None):
    if r.status_code not in [200,201,204]:
        try:
            header = inst.client_header
        except:
            header = inst.auth_head
        raise APIError(f"An API Error Occured [{r.status_code} {r.reason}]\nSent Headers: {header}\nReceived Kwargs: {json}\nURL: {r.url}\n\n")

def process_query(path,kwargs,given_kwargs):
    processed_kwargs = {i:given_kwargs[i] for i in kwargs if i in given_kwargs}
    if len(processed_kwargs)!=0:
        path += "?"
        for i in processed_kwargs:
            path += f"{i}={processed_kwargs[i]}&"
        path = path[:-1]
    return path

def valid_kwargs(kwargs,expected_args):
    if {"valid"} == {"valid" if i in expected_args else "invalid" for i in kwargs.keys()}:
        return True
    else:
        raise InvalidArguments(f'Unexpected Keyword(s) {{if i not in expected_args for i in kwargs.keys()}}')
        return False

def add_audit_reason(kwargs,headers):
    if "reason" in kwargs:
        headers["X-Audit-Log-Reason"] = kwargs["reason"]
        del kwargs["reason"]
    return kwargs,headers

def Obrray(obj_list,Object,header=False):
    # print(obj_list,Object,header)
    if obj_list == None or Object == None:
        return obj_list
    elif type(obj_list) == list:
        return [Object(**i) if header==False else Object(**{**i,**{"__client__":self.client_header}}) for i in obj_list]
    else:
        raise InvalidArguments("Tried to iterate a Non-Sequential Data Type")
