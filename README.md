# http11
An asynchronous (simple) HTTP 1.1 client and server implementation in python.

- You need python 3.7+
- (To be) asyncio installed


#### How a request looks like:

```
GET /index.html HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.example.com
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive
```

#### How a response look like:

```
HTTP/1.1 200 OK
Server: Tornado/4.3
Date: Wed, 18 Oct 2017 14:19:11 GMT
Content-type: text/html; charset=UTF-8
Content-Length: 13

Hello, world!
```