import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.scf.v20180416 import scf_client, models

class TC(object):
    def __init__(self, secretId, secretKey, endpoint="scf.tencentcloudapi.com", region_id="ap-hongkong", function_name=None):
        cred = credential.Credential(secretId, secretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = endpoint
    
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = scf_client.ScfClient(cred, region_id, clientProfile)
        
        self._func_name = function_name
    
    def call(self, url: str, method: str, function_name: str = None):
        assert (self._func_name or function_name), "function_nam is None"
        req = models.InvokeRequest()
        params = {
            "FunctionName": self._func_name or function_name,
            "ClientContext": json.dumps({"url": url, "method": method})
        }
        req.from_json_string(json.dumps(params))
        resp = self.client.Invoke(req)
        return resp.Result

class Jump(object):
    def __init__(self, secretId, secretKey, function_name=None):
        self.tc = TC(secretId, secretKey, function_name=function_name)
    
    def call(self, method, url):
        resp = self.tc.call(url=url, method=method)
        return self.parse_resp(resp)
    
    def parse_resp(self, resp):
        return json.loads(resp.RetMsg)
        
    def get(self, url):
        return self.call(method="GET", url=url)
    
    def post(self, url):
        return self.call(method="POST", url=url)
    

if __name__ == '__main__':
    j = Jump("", "", "tc_request")
    res = j.get("http://www.baidu.com")
