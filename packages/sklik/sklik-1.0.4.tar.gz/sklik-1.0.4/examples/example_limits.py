from sklik import SklikApi

token = "<sklik_token>"
sklik = SklikApi.init(token)

response = sklik.call("api", "limits")["batchCallLimits"]
print(response)
