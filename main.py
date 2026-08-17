import requests

# Yahan seedha apna token aur ID daal (Sirf test ke liye)
t = "8913665698:AAE4KqNbiJEM1VLnTIwXdOKuJGVteP2v0Tw"
c = "8193076289"

url = f"https://api.telegram.org/bot{t}/sendMessage"
r = requests.post(url, json={"chat_id": c, "text": "Oracle is Zinda!"})
print(f"RESPONSE: {r.text}")
