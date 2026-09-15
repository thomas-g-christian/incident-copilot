# Okta authentication runbook

Source (official): https://developer.okta.com/docs/reference/error-codes/

Use this when an incident mentions Okta, SSO, OAuth, JWT, 401, 403, invalid token, MFA, password expired, or Okta error codes like E0000004 / E0000011.

## Invalid token (E0000011) and SSO 401

Use this chunk when SSO, Okta, Secret Server, HTTP 401, **invalid token**, or **E0000011**.

1. Capture HTTP status, `errorCode`, `errorSummary`, and **errorId** from the API body. `errorId` is what Okta Support uses.
2. **E0000011** = Invalid token provided (401). Check the Authorization header, expiry, and whether the token was issued for this client/app. Session terminated after SSO often lands here, not on NTFS.
3. Related 401/403: E0000004 authentication failed, E0000005 invalid session, E0000006 access denied, E0000064 password expired, E0000068 MFA, E0000069 user locked.
4. Do not paste the token. If it was pasted, rotate it (`pci_do_not_paste_pan.md`).
5. Full catalog is below. IIS 401.x without an Okta `errorCode` is `iis_codes.md`.

## Support next steps (incident copilot)

1. Capture HTTP status, `errorCode`, `errorSummary`, and `errorId` from the API body. `errorId` is what Okta Support uses.
2. Do not paste PAN, passwords, or recovery answers into tickets or this copilot.
3. Match the `errorCode` in the catalog below.
4. Common auth failures:
   - E0000004 Authentication failed (401)
   - E0000011 Invalid token (401)
   - E0000005 Invalid session (403)
   - E0000006 Access denied / missing permission (403)
   - E0000064 Password expired (401)
   - E0000068 Invalid MFA passcode (403)
   - E0000069 User locked (403)
   - E0000085 Sign-on denied (403)
   - E0000207 Incorrect username or password (401)
5. Check Authorization header, HTTP verb, org feature flags, and whether the token was issued for this client/app.
6. Rate limits: E0000047, E0000109, E0000118, E0000133, and related 429 codes — wait and retry; do not hammer the API.
7. If the app uses OIDC redirect, also check `error` / `error_description` query params on `redirect_uri`.

---

# Okta API error codes and descriptions

Complete list of errors the Okta API returns. All errors include:

| Property | Description |
|---|---|
| errorCode | Okta code for this type of error |
| errorSummary | Short description; sometimes includes request-specific detail |
| errorLink | Okta code for this type of error |
| errorId | Unique id for this error; give to Okta Support |
| errorCauses | Optional further cause information |

## HTTP status codes seen with these errors

202 Accepted; 400 Bad Request; 401 Unauthorized; 403 Forbidden; 404 Not Found; 405 Method Not Allowed; 406 Not Acceptable; 409 Conflict; 410 Gone; 412 Precondition Failed; 414 URI Too Long; 422 Unprocessable Entity; 423 Locked; 429 Too Many Requests; 500 Internal Server Error; 501 Not Implemented; 502 Bad Gateway; 503 Service Unavailable; 504 Gateway Timeout.

---

## Error catalog

E0000001 — API validation exception — 400 — API validation failed; endpoint precondition violated. Check that endpoint's docs.

E0000002 — Illegal API argument exception — 400 — The request was not valid: {0}

E0000003 — Reader exception — 400 — The request body was not well-formed.

E0000004 — Authentication exception — 401 — Authentication failed

E0000005 — Invalid session exception — 403 — Invalid session

E0000006 — Access denied exception — 403 — You do not have permission to perform the requested action

E0000007 — Resource not found exception — 404 — Not found: {0}

E0000008 — Not found exception — 404 — The requested path was not found

E0000009 — Internal server error — 500 — Internal Server Error

E0000010 — Read only database exception — 503 — Service is in read only mode

E0000011 — Invalid token exception — 401 — Invalid token provided

E0000012 — Unsupported media type — 404 — Unsupported media type

E0000013 — Invalid client app exception — 403 — Invalid client app id

E0000014 — Update credentials failed exception — 403 — Update of credentials failed

E0000015 — Feature not enabled exception — 401 — You do not have permission to access the feature you are requesting

E0000016 — Activate user failed exception — 403 — Activation failed because the user is already active

E0000017 — Reset password failed exception — 403 — Password reset failed

E0000018 — Servlet request binding exception — 400 — Bad request. Accept and/or Content-Type headers are likely not set.

E0000019 — HTTP media type not acceptable exception — 400 — Accept and/or Content-Type headers likely do not match supported values.

E0000020 — Illegal argument exception — 400 — Bad request.

E0000021 — HTTP media type not supported exception — 400 — Accept and/or Content-Type headers likely do not match supported values.

E0000022 — HTTP request method not supported exception — 405 — Endpoint does not support this HTTP method. Check verb, authorization header, API access, user authorization, org features, and whether the OAuth provider accepts Okta-issued tokens.

E0000023 — App user exception — 403 — Operation failed because user profile is mastered under another system

E0000024 — Unsupported app metadata operation exception — 400 — This operation on app metadata is not yet supported.

E0000025 — Assign app version failed exception — 400 — App version assignment failed.

E0000026 — API endpoint deprecated exception — 404 — This endpoint has been deprecated.

E0000027 — Group push exception — 400 — Group push bad request: {0}

E0000028 — Missing servlet request parameter exception — 400 — The request is missing a required parameter.

E0000029 — Invalid paging exception — 400 — Invalid paging request.

E0000030 — Invalid date exception — 400 — Dates must be yyyy-MM-dd'T'HH:mm:ss.SSSZZ (example 2013-01-01T12:00:00.000-07:00).

E0000031 — Invalid search criteria exception — 400 — Invalid search criteria.

E0000032 — Unlock forbidden exception — 403 — Unlock is not allowed for this user.

E0000033 — Search request exception — 400 — Cannot specify a search query and filter in the same request.

E0000034 — Forgot password not allowed exception — 403 — Forgot password not allowed on specified user.

E0000035 — Change password not allowed exception — 403 — Change password not allowed on specified user.

E0000036 — Change recovery question not allowed exception — 403 — Change recovery question not allowed on specified user.

E0000037 — Type mismatch exception — 400 — Type mismatch exception. {0}

E0000038 — User operation forbidden exception — 403 — This operation is not allowed in the user's current status.

E0000039 — Change app instance failed exception — 403 — Operation on application settings failed.

E0000040 — Duplicate instance label exception — 400 — Application label must not match an existing application label.

E0000041 — Password option argument exception — 400 — Credentials should not be set on this resource based on the scheme.

E0000042 — Set redirect url failed exception — 403 — Setting the error page redirect URL failed.

E0000043 — Self assign org apps not enabled exception — 403 — Self service application assignment is not enabled.

E0000044 — Self assign not supported exception — 403 — Self service application assignment is not supported.

E0000045 — Field mapping API exception — 400 — Field mapping bad request.

E0000046 — Deactivate app user forbidden exception — 403 — Deactivate application for user forbidden.

E0000047 — Too many requests exception — 429 — API call exceeded rate limit due to too many requests.

E0000048 — OPP entity not found exception — 404 — Entity not found exception.

E0000049 — OPP invalid SCIM data from SCIM implementation exception — 500 — Invalid SCIM data from SCIM implementation.

E0000050 — OPP invalid SCIM data from client exception — 400 — Invalid SCIM data from client.

E0000051 — OPP no response from SCIM implementation exception — 500 — No response from SCIM implementation.

E0000052 — OPP endpoint not implemented exception — 501 — Endpoint not implemented.

E0000053 — OPP invalid SCIM filter — 400 — Invalid SCIM filter.

E0000054 — OPP invalid pagination properties — 400 — Invalid pagination properties.

E0000055 — OPP duplicate group — 409 — Duplicate group.

E0000056 — Delete app instance forbidden exception — 403 — Delete application forbidden.

E0000057 — Policy deny exception — 403 — Access to this application is denied due to a policy.

E0000058 — Policy factor required exception — 403 — Access to this application requires MFA: {0}

E0000059 — OPP connector settings test failure — 400 — Connector configuration could not be tested. Check URL and authentication parameters.

E0000060 — Unsupported operation — 501 — Unsupported operation.

E0000061 — Tab exception — 403 — Tab error: {0}

E0000062 — Duplicate app assignment — 409 — The specified user is already assigned to the application.

E0000063 — Invalid parameter combination exception — 400 — Invalid combination of parameters specified.

E0000064 — Password expired exception — 401 — Password is expired and must be changed.

E0000065 — App metadata internal server exception — 500 — Internal error processing app metadata.

E0000066 — Mim apns not configured exception — 400 — APNS is not configured, contact your admin

E0000067 — Factor service timeout exception — 504 — Factors Service Error.

E0000068 — Factor invalid code exception — 403 — Invalid Passcode/Answer

E0000069 — Factor user locked exception — 403 — User Locked

E0000070 — Factor waiting for ack exception — 202 — Waiting for ACK

E0000071 — Mim unsupported version exception — 400 — Unsupported OS Version: {0}

E0000072 — Mim enrollment disallowed exception — 403 — MIM policy settings have disallowed enrollment for this user

E0000073 — Factor user rejected code exception — 403 — User rejected authentication

E0000074 — Factor service exception — 400 — Factor Service Error

E0000075 — App user profile push constraint exception — 403 — Cannot modify the {0} attribute because it has a field mapping and profile push is enabled.

E0000076 — App user profile mastering constraint exception — 405 — Cannot modify the app user because it is mastered by an external app.

E0000077 — Read only attribute exception — 403 — Cannot modify the {0} attribute because it is read-only.

E0000078 — Immutable attribute exception — 403 — Cannot modify the {0} attribute because it is immutable.

E0000079 — Illegal auth state exception — 403 — This operation is not allowed in the current authentication state.

E0000080 — Password policy violation exception — 403 — The password does not meet the complexity requirements of the current password policy.

E0000081 — System scope attribute exception — 403 — Cannot modify the {0} attribute because it is a reserved attribute for this application.

E0000082 — Factor passcode replayed exception — 403 — Each code can only be used once. Wait for a new code.

E0000083 — Factor time window exceeded exception — 403 — PassCode is valid but exceeded time window.

E0000084 — App evaluation exception — 403 — App evaluation error.

E0000085 — Sign on denied exception — 403 — You do not have permission to access your account at this time.

E0000086 — Policy activation exception — 403 — This policy cannot be activated at this time.

E0000087 — Invalid recovery answer exception — 403 — The recovery question answer did not match our records.

E0000088 — Org Creator API subdomain already exists exception — 400 — An object with this field already exists.

E0000089 — Org Creator API name validation exception — 400 — Org Creator API name validation exception.

E0000090 — Duplicate role assignment exception — 409 — The role specified is already assigned to the user.

E0000091 — Illegal role assignment exception — 400 — The provided role type was not the same as required role type.

E0000092 — Policy allow with conditions exception — 403 — Access to this application requires re-authentication: {0}

E0000093 — Too many target records exception — 400 — Target count limit exceeded

E0000094 — Complex filter exception — 400 — The provided filter is unsupported.

E0000095 — Recovery forbidden for unknown user exception — 403 — Recovery not allowed for unknown user.

E0000096 — Idp certificate conflict exception — 409 — This certificate has already been uploaded with kid={0}.

E0000097 — Mobile phone not verified exception — 403 — There is no verified phone number on file.

E0000098 — Phone number parse exception — 400 — This phone number is invalid.

E0000099 — International SMS call not enabled exception — 403 — Only numbers located in US and Canada are allowed.

E0000100 — Search not available exception — 503 — Unable to perform search query.

E0000101 — Invalid hosted mobile app — 400 — Issue with the app binary file you uploaded. {0}

E0000102 — Invalid yubikey state exception — 403 — YubiKey cannot be deleted while assigned to a user. Deactivate via reset MFA first.

E0000103 — OEM command already queued — 403 — Action on device already in queue or in progress

E0000104 — OEM device already locked — 403 — Device is already locked

E0000105 — Invalid or expired recovery token — 403 — Account recovery link expired or previously used.

E0000107 — Transition state exception — 403 — The entity is not in the expected state for the requested transition.

E0000108 — OEM generic duplicate resource — 409 — OEM generic duplicate resource.

E0000109 — SMS too many requests exception — 429 — An SMS was recently sent. Wait 30 seconds.

E0000110 — Invalid or expired transaction token — 403 — Link expired or previously used.

E0000111 — Read only object exception — 403 — Cannot modify the {0} object because it is read-only.

E0000112 — Update activating user exception — 409 — Cannot update this user; still activating. Retry in a few minutes.

E0000113 — Factor additional challenge exception — 409 — {0}.

E0000115 — Hosted mobile app service exception — 503 — Issue while uploading the app binary file. {0}

E0000116 — Hosted mobile app upload exception — 400 — {0}

E0000117 — Inactive user forbidden exception — 403 — Cannot assign apps or update app profiles for an inactive user.

E0000118 — Email too many requests exception — 429 — An email was recently sent. Wait 5 seconds.

E0000119 — User locked recovery exception — 403 — Your account is locked. Contact your administrator.

E0000120 — Org Creator API custom domain validation exception — 400 — Custom domain already in use by another organization.

E0000121 — Invalid phone extension — 400 — Invalid phone extension.

E0000122 — Media type not accepted exception — 406 — Accept header did not contain application/json

E0000123 — Enum mismatch exception — 400 — Array specified in enum field must match const values in oneOf field.

E0000124 — Expire on create requires password exception — 400 — To create a user and expire password immediately, a password must be specified

E0000125 — Expire on create requires activation exception — 400 — To create a user and expire password immediately, activate must be true

E0000126 — Self service not supported exception — 400 — Self service is not supported with the current settings.

E0000127 — Linked object definition exception — 409 — Invalid linked object definition. {0}

E0000131 — Feature validation exception — 400 — {0}

E0000132 — Client registration already active exception — 400 — Registration is already active for this user, client and device combination

E0000133 — Phone call too many requests exception — 429 — A phone call was recently made. Wait 30 seconds.

E0000134 — Callback execution exception — 502 — Okta could not communicate correctly with an inline hook.

E0000135 — Callback error — 400 — An inline hook responded with an error.

E0000136 — Mobile phone conflict exception — 409 — Mobile phone conflict exception.

E0000137 — Callback timeout — 504 — Okta did not receive a response from an inline hook.

E0000138 — Telephony internal error — 500 — Internal error with call provider(s).

E0000139 — Telephony provider error — 503 — Telephony provider error.

E0000140 — Telephony opt out error — 400 — Telephony opt out error.

E0000141 — Feature update error — 400 — Feature cannot be enabled or disabled due to dependency conflicts.

E0000142 — Delete user type exception — 403 — This User Type cannot be deleted.

E0000143 — App instance operation not allowed exception — 403 — App instance operation not allowed.

E0000145 — User entity conversion type error — 409 — Some search results cannot be parsed; user schema inconsistent with stale profile data.

E0000146 — SMS roadblock exception — 429 — Org reached SMS request limit for a 24 hour period.

E0000147 — Call roadblock exception — 429 — Org reached call request limit for a 24 hour period.

E0000148 — Policy violation exception — 403 — Cannot modify/disable this authenticator because it is enabled in one or more policies. {0}

E0000149 — HTTP request not acceptable — 406 — The HTTP request is not acceptable.

E0000150 — SMS rate limit exception — 403 — SMS request limit reached; try later.

E0000151 — Call rate limit exception — 403 — Call request limit reached; try later.

E0000152 — Illegal device status exception — 403 — Illegal device status, cannot perform action.

E0000153 — Invalid device id exception — 410 — Invalid device id, it no longer exists.

E0000154 — Invalid factor id exception — 410 — Invalid factor id, it is not currently active.

E0000155 — User not active exception — 423 — User is not currently active.

E0000156 — Invalid user id exception — 410 — Invalid user id; user does not exist or was deleted.

E0000157 — Authenticator already exists exception — 409 — Another authenticator with key: {0} is already active.

E0000158 — Non user verification compliance enrollment exception — 400 — Invalid enrollment. User verification required.

E0000159 — Non fips compliance okta verify enrollment exception — 400 — Invalid enrollment. FIPS compliance required.

E0000161 — Domain already exists exception — 403 — Unique domain name required.

E0000162 — Domain limit exception — 403 — Domain count limit reached.

E0000163 — Domain not found exception — 404 — Domain ID not found.

E0000165 — Domain not verified exception — 403 — Domain not verified.

E0000166 — Captcha limit exception — 403 — At most one CAPTCHA instance per org.

E0000167 — Deactivate idp in use by authenticator exception — 403 — {0}

E0000168 — Captcha associated with org exception — 403 — CAPTCHA is associated with org-wide settings; unassociate before removing.

E0000170 — Org Creator API subdomain reserved exception — 400 — Reserved subdomain value.

E0000171 — Org Creator API subdomain locked exception — 400 — Subdomain already in use by a different request.

E0000172 — Org Creator API subdomain name too long exception — 400 — Subdomain exceeds max length.

E0000174 — Device condition dependency exception — 403 — Cannot disable Okta FastPass; used by application sign-on policies with device conditions.

E0000176 — Log streaming create failed — 400 — Failed to create LogStreaming event source. {0}

E0000177 — Log streaming delete failed — 400 — Failed to delete LogStreaming event source. {0}

E0000178 — Cannot delete realm exception — 400 — This realm cannot be deleted. {0}

E0000179 — Externally sourced attribute exception — 400 — There is a required attribute that is externally sourced.

E0000180 — Suspended factor exception — 423 — Factor id is currently not active.

E0000181 — Dns challenge not found exception — 503 — Service temporarily unavailable.

E0000182 — Email customization default already exists exception — 409 — A default email template customization already exists.

E0000183 — Email customization language already exists exception — 409 — Customization for that language already exists.

E0000184 — Email customization cannot delete default exception — 409 — A default email template customization can't be deleted.

E0000185 — Email customization cannot clear default exception — 409 — isDefault of the default customization can't be set to false.

E0000186 — SMS free org roadblock exception — 429 — Free tier org reached SMS limit for a 30 day period.

E0000187 — Push provider dependency exception — 409 — Cannot delete push provider; used by a custom app authenticator.

E0000188 — Domain update conflict exception — 409 — Domain update conflict exception.

E0000189 — Email template invalid recipients exception — 422 — This template does not support the recipients value.

E0000190 — Delete ldap interface forbidden exception — 403 — Delete LDAP interface instance forbidden.

E0000191 — Transaction not found exception — 404 — Verification timed out. Please try again.

E0000192 — Assign admin privilege to group with rules exception — 400 — Roles cannot be granted to groups with group membership rules. {0}

E0000193 — Group member count exceeds limit exception — 400 — Roles only for groups with 5000 or fewer users. {0}

E0000194 — Non applicable group type exception — 400 — Roles only for Okta, AD, and LDAP groups. {0}

E0000195 — API conflict exception — 409 — Api validation failed due to conflict: {0}

E0000197 — Email domain already exists exception — 409 — Unique email domain name required.

E0000198 — Email domain not found exception — 404 — Email domain not found.

E0000200 — Brand cannot delete default exception — 409 — A default brand cannot be deleted.

E0000201 — Brand cannot delete already assigned exception — 409 — Brand associated with a custom domain or email domain cannot be deleted.

E0000202 — Brand name already exist exception — 409 — Brand name already exists.

E0000203 — Brand domain mapping failure exception — 409 — Failed to associate this domain with the given brandId.

E0000204 — SMS rate limit exception 429 — 429 — SMS request limit; try later.

E0000205 — Call rate limit exception 429 — 429 — Call request limit; try later.

E0000207 — Incorrect username or password exception — 401 — The username and/or password you entered is incorrect.

E0000208 — Access token bad request exception — 400 — Failed to get access token. Invalid request, reason: {0}.

E0000209 — Aaguid group violation exception — 400 — {0} cannot be modified/deleted; used in an Enroll Policy.

E0000211 — Built in groups type exception — 400 — Roles cannot be granted to built-in groups: {0}

E0000212 — Invalid origin header exception — 403 — Origin validation failed.

E0000213 — Cannot update page content for default brand exception — 403 — Cannot update page content for the default brand.

E0000214 — User has no enrollments that are ciba enabled — 400 — User has no custom authenticator enrollments with CIBA as a transactionType

E0000215 — API endpoint no longer available — 410 — This endpoint has been deprecated.

E0000217 — Email domain invalid status exception — 400 — Cannot validate email domain in current status.

E0000218 — Email domain validation exception — 400 — Email domain could not be verified by mail provider.

E0000219 — Phishing resistance policy error — 403 — Action would leave 0 phishing-resistant authenticators while policy requires them. Enable FIDO2/WebAuthn or remove the constraint. Policy rules: {0}

E0000220 — Brand limit exception — 403 — Brand count limit reached.

E0000221 — Realm limit exceeded exception — 403 — Maximum number of realms reached. An org cannot have more than {0} realms.

E0000222 — Email server already enabled exception — 400 — Only one SMTP server can be enabled at a time.

E0000223 — Email server connection failed exception — 400 — Connection with the specified SMTP server failed.

E0000224 — Email server auth failed exception — 400 — Authentication with the specified SMTP server failed.

E0000225 — Email server max enrolled exception — 400 — Maximum enrolled SMTP servers reached. Max {0}.

E0000226 — Required telephony inline hook enabled for phone authenticator exception — 400 — Active telephony inline hook required to use the Phone authenticator.

E0000227 — Non applicable app as principal type exception — 400 — Roles can only be granted to service application type

E0000228 — SMS template customization not allowed exception — 403 — SMS template customization isn't permitted.

E0000229 — Non bio or pin user verification compliance enrollment exception — 400 — Invalid enrollment. Biometrics with Pin fallback required.

E0000230 — Idp for custom idp authenticator already in use exception — 409 — Another authenticator is already associated with idpId: {0}.

E0000231 — Etag not matched exception — 412 — ETag value doesn't match.

E0000232 — Duplicate authenticator nickname exception — 400 — Another authenticator enrollment already exists with the same nickname.

E0000233 — SMS free org okta verify setup link bloc exception — 403 — Okta Verify SMS setup link is paid-only. Upgrade free tier org.

E0000235 — Resource selectors exception — 400 — Resource Selector: {0}

E0000236 — Email customization invalid bcp47 locale format exception — 400 — Language doesn't conform to BCP 47.

E0000237 — Email customization test locale not permitted exception — 400 — Language isn't permitted for email customization.

E0000239 — Policy lock exception — 423 — Policy priorities are being reconciled. Try again later.

E0000240 — Agent time out — 502 — Request timed out waiting for agent.

E0000241 — No connected agents — 504 — No connected agents.

E0000242 — Invalid etag exception — 400 — ETag syntax is invalid.

E0000243 — API validation exception with no message — 400 — Bad request.

E0000244 — Email customization multiple defaults exception — 409 — Conflicting default customizations. Discard changes and reset templates.

E0000245 — Knowledge second and access policy conflict exception — 400 — Authentication method chains include a knowledge method in the first step. Require a possession factor first: {0}

E0000246 — Deactivate authenticator method in use by authentication policy method chain exception — 403 — Authentication method is in use by policies: {0}

E0000247 — Okta telephony disabled exception — 403 — Org doesn't support SMS or Voice authentication. Select another method.

E0000248 — Deactivate idp in use by okta account management policy exception — 403 — Id Proofing IdP is used in Okta Account Management Policy rules. {0}

E0000249 — Missing group rule policy exception — 409 — Group rules are still being set up. Try again later.

E0000250 — Idp in use by asop gsp policy exception — 403 — Cannot {0} {1}; Trust claims not enabled on any other IdP. Update {2} and {3} policies.

E0000251 — Idp in use by gsp policy exception — 403 — Cannot {0} {1}; Trust claims not enabled on any other IdP. Update {2} policies.

E0000252 — Idp in use by asop policy exception — 403 — Cannot {0} {1}; Trust claims not enabled on any other IdP. Update {2} policies.

E0000253 — User type initialization in progress exception — 409 — User type is still being initialized. Try again later.

E0000254 — Email template settings update conflict exception — 409 — Another request already updating this email template settings. Try later.

E0000255 — App instance with published version status cannot be deleted exception — 403 — App instance with Published version status can't be deleted.

E0000256 — Response header too long — 414 — Response header too large to process.

E0000257 — Brand well known uri cannot update default brand exception — 405 — Cannot update the content for the default brand.

E0000258 — Brand well known uri invalid path exception — 404 — Path not supported. Valid values: [{0}].

E0000259 — Breached credential password expire fail during login exception — 403 — Login not allowed. Reset password or contact administrator.

E0000260 — Dev org sign on denied exception — 403 — This developer org has been deactivated. Contact org admin.

E0000261 — Corrupt linked object multiple values exception — 500 — Linked object {0} is invalid for this user.

E0000262 — Idp in use by device posture idp exception — 403 — Device Assurance or Device Signal Collection policies use Device Posture IdP signals. Update those policies first.

E0000263 — Duplicate standard iam role assignment exception — 409 — Duplicate standard role assignment to an admin

E0000264 — Required active custom telephony provider credential for phone authenticator exception — 400 — Active telephony inline hook or custom telephony provider credential required for Phone authenticator.

E0000265 — Device registration already in progress exception — 409 — Device registration is already in progress for this device.

E0000266 — Email server failed to get access token exception — 400 — Failed to get access token for SMTP server. {0}

E0000267 — Admin home page denied exception — 403 — Access to the Home Page is restricted for this organization.

E0000268 — Role manager lock conflict exception — 409 — Another request is changing role assignments. Try again.

E0000269 — Script config missing — 403 — The script config for instanceId {0} is not available.

---

## OpenID Connect and Social Login redirect errors

When Okta must pass an error to a downstream app through `redirect_uri`, the code is query parameters `error` and `error_description`.

Example: if redirect_uri is https://example.com then ACCESS_DENIED becomes:

https://example.com?error=access_denied&error_description=The%20resource%20owner%20or%20authorization%20server%20denied%20the%20request

| error | meaning |
|---|---|
| unauthorized_client | Client isn't authorized to request an authorization code using this method. |
| access_denied | Resource owner or authorization server denied the request. |
| unsupported_response_type | Authorization server doesn't support obtaining an authorization code using this method. |
| unsupported_response_mode | Authorization server doesn't support the requested response mode. |
| invalid_scope | Requested scope is invalid, unknown, or malformed. |
| server_error | Unexpected condition prevented fulfilling the request. |
| temporarily_unavailable | Temporary overload or maintenance. |
| invalid_client | Specified client isn't valid. |
| login_required | Client specified not to prompt, but the user isn't signed in. |
| invalid_request | Request parameters aren't valid. |
| user_canceled_request | User canceled the social sign-in request. |

Official page: https://developer.okta.com/docs/reference/error-codes/
