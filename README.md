# WhiteRabbit-Proxy
This is a proxy server script which helps to achieve an SQL injection on HTB WhiteRabbit Box.

# Short Remark
This repo isn't an exploit itself this is just a proxy server which forwards your requests.

# Description
The WhiteRabbit box has a webhook with a potential SQL injection in Get Current Phishing Score node. However we can't 
simply achieve this SQL injection with sqlmap, because end point is protected by HMAC signature. Each time we when
we send an unsigned/ or an invalid payload the server responds with "Invalid Signature". So this script just accepts 
a payload in a query parameter, calculates HMAC signature and forwards your request to the endpoint.


# Usage

1. Add a webhook url to /etc/hosts

2. Launch script with a python:
   
   ```python3 proxy.py```

3. Proxy will start listening on port 10000, so you may reach the endpoint with following command:

   ```curl http://localhost:10000/?query=SOMETHING```

4. Now you can make an automatic SQL injection with a command like:
   
   ```sqlmap 'http://localhost:10000/?query=test' -p query --level 5 --risk 3 --batch```

5. The server will be showing all the requests performed by sqlmap, so it might be interesting to watch the
process or try to achieve end point manually with different payloads in order to better understand what is
going on.


