# WhiteRabbit-Proxy
This is a proxy server script in order to help to achieve SQL injection in HTB WhiteRabbit Box

# Short Remark
This repo isn't an exploit itself this is just a proxy server which can help you to achieve SQL Injection in
the WhiteRabbit HTB box.

# Description
The WhiteRabbit box has a webhook with a potential SQL injection in it. However we can't simply achieve this
SQL injection with sqlmap, because end point is protected with HMAC signature. Each time we send an unsigned/
or an invalid payload the server responds with "Invalid Signature". So this script just accepts a payload
in a query parameter, calculates HMAC signature and forwards you request to the endpoint.


# Usage

1. Add a webhook url to /etc/hosts

2. Launch script with a python:
   
   ```python3 proxy.py```

3. Proxy will start listening on port 10000, so you reach the endpoint with following command:

   ```curl http://localhost:10000/?query=SOMETHING```

4. Now you can make an automatic SQL injection with a command like:
   
   ```sqlmap 'http://localhost:10000/?query=test' -p query --level 5 --risk 3 --batch```


