# IIS HTTP status codes

Use this catalog when the incident is an IIS / ASP.NET site status (401.x, 403.x, 404.x, 500.x, 502.x, 503.x). Substatus lives in the IIS log (`sc-status` and `sc-substatus`), not always in the browser.

## 502 / ARR / bad gateway

Use this chunk when IIS or ARR returns **502**, **502.3**, bad gateway, or a forwarder connection error while proxying to a vendor.

1. Get **sc-status** and **sc-substatus** from the IIS log (W3C: `sc-status sc-substatus sc-win32-status`). Browser “502” is not enough.
2. **502.3** = Bad Gateway: Forwarder Connection Error (ARR). **502.4** = No Server (ARR). Site bindings can be fine while ARR still returns 502.3.
3. We were the proxy; the backend or vendor did not complete. Capture the vendor request id, then use `vendor_api.md` for the vendor body/SLA.
4. Do not skip the IIS substatus just because the ticket already names a vendor.

## Support next steps (incident copilot)

1. Get the **status and substatus** from the IIS log (W3C: `sc-status sc-substatus sc-win32-status`). Browser “500” is not enough.
2. Common hits:
   - **401.1 / 401.2** — logon / auth config (then see `okta_auth.md` if SSO/Okta).
   - **401.3 / 403.1–403.3** — NTFS or IIS execute/read/write (then see `permissions.md`).
   - **403.4 / 403.5** — SSL required.
   - **404.0 / 404.4** — missing file or no handler.
   - **500.0 / 500.19** — module error or bad `web.config` / `applicationHost.config`.
   - **500.11 / 500.12 / 503.0** — app pool shutting down, restarting, or stopped.
   - **502.x** — bad gateway / ARR / timeout talking to a backend (then see `vendor_api.md`).
   - **408** — request timed out at IIS (then see `sql_timeout.md` if the page was waiting on SQL).
3. Check app-pool identity, site bindings, and whether the worker process is running.
4. Do not paste PAN, passwords, or full `web.config` connection strings into this copilot. See `pci_do_not_paste_pan.md`.
5. Look up the exact code in the catalog below.

---

HTTP Status Codes
Code	Description	Notes
100	Continue	Initial part of the request has been received and hasn't yet been rejected by the server. The server intends to send a final response after the request has been fully received and acted upon.
101	Switching protocols	Server understands and is willing to comply with client's request for a change in the application protocol being used.

200	OK	The client request was successfully processed.
201	Created	The client request has been fulfilled and has resulted in one or more new resources being created.
202	Accepted	The client request has been accepted for processing, but the processing hasn't been completed.
203	Nonauthoritative information	The client request was successful but the enclosed content has been modified from the response of the origin server.
204	No content	The server has successfully fulfilled the request and that there's no additional content to send in the response content.
205	Reset content	The server has fulfilled the request and expects the user agent to reset the "document view," which caused the request to be sent, to its original state as received from the origin server.
206	Partial content	The server is successfully fulfilling a range request for the target resource by transferring one or more parts of the selected representation.

301	Moved permanently	The target resource has been assigned a new permanent URI and any future references to this resource ought to use one of the enclosed URIs.
302	Object moved	The target resource resides temporarily under a different URI. Since the redirection might be altered on occasion, the client ought to continue to use the target URI for future requests
304	Not modified	A conditional GET or HEAD request has been received and would have resulted in a 200 (OK) response if it weren't for the fact that the condition evaluated to false.
307	Temporary redirect	The client browser requests a document that is already in the cache. And the document hasn't been modified since it was cached. The client browser uses the cached copy of the document instead of downloading the document from the server.

400	Bad request	The request couldn't be understood by the server due to malformed syntax. The client shouldn't repeat the request without modifications. For more information, see Troubleshooting HTTP 400 Errors in IIS.
401	Access denied	The request hasn't been applied because it lacks valid authentication credentials for the target resource.
403	Forbidden	The server understood the request but refuses to fulfill it.
404	Not found	The origin server didn't find a current representation for the target resource or isn't willing to disclose that one exists.
405	Method not allowed	The method received in the request-line is known by the origin server but not supported by the target resource.
406	Not acceptable	The client browser doesn't accept the MIME type of the requested resource.
408	Request timed out	The server didn't receive a complete request message within the time that it was prepared to wait.
412	Precondition failed	One or more conditions given in the request header fields evaluated to false when tested on the server.
413	Request entity too large	The HTTP request payload is too large.

400.1	Invalid Destination Header
400.2	Invalid Depth Header
400.3	Invalid If Header
400.4	Invalid Overwrite Header
400.5	Invalid Translate Header
400.6	Invalid Request Body
400.7	Invalid Content Length
400.8	Invalid Timeout
400.9	Invalid Lock Token
400.10	Invalid X-Forwarded-For (XFF) header
400.11	Invalid WebSocket request

400.601	Bad client request (ARR)
400.602	Invalid time format (ARR)
400.603	Parse range error (ARR)
400.604	Client gone (ARR)
400.605	Maximum number of forwards (ARR)
400.606	Asynchronous competition error (ARR)

401.1	Logon failed	The logon attempt is unsuccessful probably because of a user name or a password that is invalid.
401.2	Logon failed due to server configuration	This HTTP status code indicates a problem in the authentication configuration settings on the server.
401.3	Unauthorized due to ACL on resource	This HTTP status code indicates a problem in the NTFS file system permissions. This problem might occur even if the permissions are correct for the file that you try to access. For example, this problem occurs if the IUSR account doesn't have access to the C:\Winnt\System32\Inetsrv directory.
401.4	Authorization failed by filter	An Internet Server Application Programming Interface (ISAPI) filter doesn't let the request be processed because of an authorization problem.
401.5	Authorization failed by ISAPI/CGI application	An ISAPI application or a Common Gateway Interface (CGI) application doesn't let the request be processed because of an authorization problem.
401.501	Access denied: concurrent request rate limit reached	Dynamic IP Restriction: too many concurrent requests were made from the same client IP.
401.502	Access denied: maximum request rate limit reached	Dynamic IP Restriction: the maximum number of requests from the same client IP within a specified time limit was reached.
401.503	Access denied: IP address denied	IP Restriction: the client IP address is included in the deny list.
401.504	Access denied: host name denied	IP Restriction: the client host name is included in the deny list. name denied.

403.1	Execute access forbidden	The appropriate level of the Execute permission isn't granted.
403.2	Read access forbidden	The appropriate level of the Read permission isn't granted. Verify that you have set up IIS to grant the Read permission to the directory. Additionally, if you use a default document, verify that the default document exists.
403.3	Write access forbidden	The appropriate level of the Write permission isn't granted. Check the IIS permissions and the NTFS file system permissions. Make sure that they're set up to grant the "Write" permission to the directory.
403.4	SSL required	The request is made over a non-secure channel. But the web application requires a Secure Sockets Layer (SSL) connection.
403.5	SSL 128 required	The server is configured to require a 128-bit SSL connection. But, the request isn't sent by using 128-bit encryption.
403.6	IP address rejected	The server is configured to deny access to the current IP address.
403.7	Client certificate required	The server is configured to require a certificate for client authentication. But the client browser doesn't have an appropriate client certificate installed. For more information, see HTTP error 403.7.
403.8	Site access denied	The server is configured to deny requests based on the Domain Name System (DNS) name of the client computer. For more information, see Dynamic IP Address restrictions.
403.9	Concurrent connections exceeded	Too many clients are trying to connect to the web server.
403.10	Forbidden: Execute access denied	The web server is configured to deny "Execute" access.
403.11	Forbidden: Password changed	A password has been changed.
403.12	Mapper denied access	The page that you want to access requires a client certificate. But, the user ID that is mapped to the client certificate is denied access to the file.
403.13	Client certificate revoked	The client browser tries to use a client certificate that was revoked by the issuing certification authority.
403.14	Directory listing denied	The server isn't configured to display a content directory listing, and a default document isn't set. For more information, see HTTP Error 403.14.
403.15	Client access licenses exceeded	The number of client access licenses has exceeded the limits on the web server.
403.16	Client certificate is untrusted or invalid	The client browser tries to use an invalid client certificate. Or the server that is running IIS doesn't trust the client certificate. For more information, see HTTP Error 403.16.
403.17	Client certificate has expired or is not yet valid	The client browser tries to use a client certificate that is expired or that isn't yet valid.
403.18	Cannot execute requested URL in the current application pool	A custom error page is configured. And the application pool of the customer error page is different with the application pool of the requested URL.
403.19	Cannot execute CGI applications for the client browser in this application pool	The identity of the application pool doesn't have the Replace a process level token user right.
403.20	Forbidden: Passport logon failed	Client requests using passport logon aren't allowed.
403.21	Forbidden: Source access denied	WebDAV requests to the source code of a resource aren't allowed.
403.22	Forbidden: Infinite depth is denied	WebDAV requests with an infinite depth aren't allowed.
403.501	Forbidden: concurrent request rate limit reached	Dynamic IP Restriction: too many concurrent requests were made from the same client IP.
403.502	Forbidden: maximum request rate limit reached	Dynamic IP Restriction: the maximum number of requests from the same client IP within a specified time limit was reached.
403.503	Forbidden: IP address denied	IP Restriction: the client IP address is included in the deny list.
403.504	Forbidden: host name denied	IP Restriction: the client host name is included in the deny list.

404.0	Not found	The file that you try to access is moved or doesn't exist.
404.1	Site Not Found	The requested website doesn't exist.
404.2	ISAPI or CGI restriction.	The requested ISAPI resource or the requested CGI resource is restricted on the computer. For more information, see HTTP Error 404.2.
404.3	MIME type restriction.	The current MIME mapping for the requested extension type is invalid or isn't configured.
404.4	No handler configured.	The file name extension of the requested URL doesn't have a handler that is configured to process the request on the Web server.
404.5	Denied by request filtering configuration.	The requested URL contains a character sequence that is blocked by the server.
404.6	Verb denied.	The request is made by using an HTTP verb that isn't configured or that isn't valid.
404.7	File extension denied.	The requested file name extension isn't allowed.
404.8	Hidden namespace.	The requested URL is denied because the directory is hidden.
404.9	Files attribute hidden.	The requested file is hidden.
404.10	Request header too long.	The request is denied because the request headers are too long.
404.11	Request contains double escape sequence.	The request contains a double escape sequence.
404.12	Request contains high-bit characters.	The request contains high-bit characters, and the server is configured not to allow high-bit characters.
404.13	Content length too large.	The request contains a Content-Length header. The value of the Content-Length header is larger than the limit that is allowed for the server. For more information, see HTTP Error 404.13 - CONTENT_LENGTH_TOO_LARGE.
404.14	Request URL too long.	The requested URL exceeds the limit that is allowed for the server.
404.15	Query string too long.	The request contains a query string that is longer than the limit that is allowed for the server.
404.16	WebDAV request sent to the static file handler	A WebDAV request wasn't processed by a WebDAV feature and was sent to the static file handler.
404.17	Dynamic content mapped to the static file handler	For more information, see HTTP Error 404.17 - Not Found.
404.18	Query string sequence denied	The request contains a query string sequence that isn't allowed.
404.19	Denied by filtering rule	The request was denied due to a Request Filtering rule.
404.20	Too Many URL Segments	The request contains too many URL segments.
404.501	Not found: concurrent request rate limit reached	Dynamic IP Restriction: too many concurrent requests were made from the same client IP.
404.502	Not found: maximum request rate limit reached	Dynamic IP Restriction: the maximum number of requests from the same client IP within a specified time limit was reached.
404.503	Not found: IP address denied	IP Restriction: the client IP address is included in the deny list.
404.504	Not found: host name denied	IP Restriction: the client host name is included in the deny list.

405.0	Method not allowed.	The request is made by using an HTTP method that isn't valid. For more information, see HTTP Error 405.0.
406.0	Not acceptable.	The request is made by using an Accept header that contains a MIME value that isn't valid.
408.0	Request timed out.	The server didn't receive a complete request message within the time that it was prepared to wait.
412.0	Precondition failed.	The request is made by using an If-Match request header that contains a value that isn't valid.
413.0	Request entity too large.	The request is made by using a payload that is too large.

500	Internal server error	The server encountered an unexpected condition that prevented it from fulfilling the request.
501	Header values specify a configuration that is not implemented	The server doesn't support the functionality required to fulfill the request.
502	Web server received an invalid response while acting as a gateway or proxy	The server, while acting as a gateway or proxy, received an invalid response from an inbound server it accessed while attempting to fulfill the request. For more information, see Troubleshooting 502 Errors in ARR.
503	Service unavailable	The server is currently unable to handle the request due to a temporary overload or scheduled maintenance, which will likely be alleviated after some delay.

500.0	Module or ISAPI error occurred.	This HTTP status code may occur for many server-side reasons. For more information, see HTTP Error 500.0 - Internal Server Error.
500.11	Application is shutting down on the web server.	The request isn't processed because the destination application pool is shutting down. Wait for the worker process to finish shutting down, and then try the request again. If this problem persists, the web application may be experiencing problems that prevent the web application from shutting down correctly.
500.12	Application is busy restarting on the web server.	The request isn't processed because the destination application pool is restarting. This HTTP status code should disappear when you refresh the page. If this HTTP status code appears again after you refresh the page, the problem may be caused by antivirus software that is scanning the Global.asa file. If this problem persists, the web application may be experiencing problems that prevent the web application from restarting correctly.
500.13	Web server is too busy.	The request isn't processed because the server is too busy to accept any new incoming requests. Typically, this HTTP status code means that the number of incoming concurrent requests exceeds the number that the IIS web application can process. This problem may occur when the performance configuration settings are set too low, the hardware is insufficient, or a bottleneck occurs in the IIS web application. A common troubleshooting method is to generate a memory dump file of the IIS processes when the error is occurring and then to debug the memory dump file.
500.15	Direct requests for Global.asax aren't allowed.	A direct request for the Global.asa file or for the Global.asax file is made.
500.19	Configuration data is invalid.	This HTTP status code occurs because of a problem in the associated applicationhost.config file or in the associated Web.config file. For more information, see HTTP Error 500.19.
500.21	Module not recognized.	
500.22	An ASP.NET httpModules configuration does not apply in Managed Pipeline mode.	
500.23	An ASP.NET httpHandlers configuration does not apply in Managed Pipeline mode.	
500.24	An ASP.NET impersonation configuration does not apply in Managed Pipeline mode.	
500.50	A rewrite error occurred during RQ_BEGIN_REQUEST notification handling. A configuration or inbound rule execution error occurred.	Here's where the distributed rules configuration is read for both inbound and outbound rules.
500.51	A rewrite error occurred during GL_PRE_BEGIN_REQUEST notification handling. A global configuration or global rule execution error occurred.	Here's where the global rules configuration is read.
500.52	A rewrite error occurred during RQ_SEND_RESPONSE notification handling. An outbound rule execution occurred.	
500.53	A rewrite error occurred during RQ_RELEASE_REQUEST_STATE notification handling. An outbound rule execution error occurred. The rule is configured to be executed before the output user cache gets updated.	
500.100	Internal ASP error.	An error occurs during the processing of an Active Server Pages (ASP) page. To obtain more specific information about the error, disable friendly HTTP error messages in the web browser. Additionally, the IIS log may show an ASP error number that corresponds to the error that occurs.

502.1	CGI application timeout.
502.2	Bad gateway: Premature Exit.
502.3	Bad Gateway: Forwarder Connection Error (ARR).
502.4	Bad Gateway: No Server (ARR).

502.2	Map request failure (ARR)
502.3	WinHTTP asynchronous completion failure (ARR)
502.4	No server (ARR)
502.5	WebSocket failure (ARR)
502.6	Forwarded request failure (ARR)
502.7	Execute request failure (ARR)

503.0	Application pool unavailable.	The request is sent to an application pool that is currently stopped or disabled. To resolve this issue, make sure that the destination application pool is started. The event log may give information about why the application pool is stopped or disabled.
503.2	Concurrent request limit exceeded.	The appConcurrentRequestLimit property is set to a value that is lower than the current number of concurrent requests. IIS doesn't allow more concurrent requests than the value of the appConcurrentRequestLimit property.
503.3	ASP.NET queue full	
503.4	FastCGI queue full	