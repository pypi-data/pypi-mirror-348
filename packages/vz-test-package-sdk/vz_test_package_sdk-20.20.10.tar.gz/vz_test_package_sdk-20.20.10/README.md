
# Getting Started with Verizon

## Introduction

The Verizon Edge Discovery Service API can direct your application clients to connect to the optimal service endpoints for your Multi-access Edge Computing (MEC) applications for every session. The Edge Discovery Service takes into account the current location of a device, its IP anchor location, current network traffic and other factors to determine which 5G Edge platform a device should connect to.

Verizon Terms of Service: [https://www.verizon.com/business/5g-edge-portal/legal.html](https://www.verizon.com/business/5g-edge-portal/legal.html)

## Install the Package

The package is compatible with Python versions `3.7+`.
Install the package from PyPi using the following pip command:

```bash
pip install vz-test-package-sdk==20.20.10
```

You can also view the package at:
https://pypi.python.org/pypi/vz-test-package-sdk/20.20.10

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| vz_m_2_m_token | `str` | M2M Session Token ([How to generate an M2M session token?](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/session-management.md#start-connectivity-management-session)) |
| environment | `Environment` | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| http_client_instance | `HttpClient` | The Http Client passed from the sdk user for making requests |
| override_http_client_configuration | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| http_call_back | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| timeout | `float` | The value to use for connection timeout. <br> **Default: 60** |
| max_retries | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| backoff_factor | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| retry_statuses | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| retry_methods | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| thingspace_oauth_credentials | [`ThingspaceOauthCredentials`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/oauth-2-client-credentials-grant.md) | The credential object for OAuth 2 Client Credentials Grant |
| vzm_2_m_token_credentials | [`VZM2MTokenCredentials`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/custom-header-signature.md) | The credential object for Custom Header Signature |
| session_token_credentials | [`SessionTokenCredentials`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/custom-header-signature-1.md) | The credential object for Custom Header Signature |

The API client can be initialized as follows:

```python
client = VerizonClient(
    vz_m_2_m_token='VZ-M2M-Token',
    thingspace_oauth_credentials=ThingspaceOauthCredentials(
        o_auth_client_id='OAuthClientId',
        o_auth_client_secret='OAuthClientSecret',
        o_auth_scopes=[
            OAuthScopeThingspaceOauthEnum.DISCOVERYREAD,
            OAuthScopeThingspaceOauthEnum.SERVICEPROFILEREAD
        ]
    ),
    vzm_2_m_token_credentials=VZM2MTokenCredentials(
        vz_m_2_m_token='VZ-M2M-Token'
    ),
    session_token_credentials=SessionTokenCredentials(
        session_token='SessionToken'
    ),
    environment=Environment.PRODUCTION
)
```

## Environments

The SDK can be configured to use a different environment for making API calls. Available environments are:

### Fields

| Name | Description |
|  --- | --- |
| production | **Default** |
| environment2 | - |
| environment3 | - |
| environment4 | - |
| environment5 | - |
| environment6 | - |
| environment7 | - |
| environment8 | - |
| environment9 | - |
| environment10 | - |
| environment11 | - |
| environment12 | - |
| environment13 | - |
| environment14 | - |
| environment15 | - |
| environment16 | - |
| environment17 | - |
| environment18 | - |
| environment19 | - |
| environment20 | - |
| environment21 | - |
| environment22 | - |
| environment23 | - |
| environment24 | - |
| environment25 | - |
| environment26 | - |
| environment27 | - |
| environment28 | - |
| environment29 | - |
| environment30 | - |
| environment31 | - |
| environment32 | - |
| environment33 | - |
| environment34 | - |
| environment35 | - |
| environment36 | - |
| environment37 | - |
| environment38 | - |
| environment39 | - |
| environment40 | - |
| environment41 | - |
| environment42 | - |
| environment43 | - |
| environment44 | - |
| environment45 | - |
| environment46 | - |
| environment47 | - |
| environment48 | - |
| environment49 | - |
| environment50 | - |
| environment51 | - |
| environment52 | - |
| environment53 | - |
| environment54 | - |
| environment55 | - |
| environment56 | - |
| environment57 | - |
| environment58 | - |
| environment59 | - |
| environment60 | - |
| environment61 | - |
| environment62 | - |
| environment63 | - |
| environment64 | - |
| environment65 | - |
| environment66 | - |
| environment67 | - |
| environment68 | - |
| environment69 | - |
| environment70 | - |
| environment71 | - |
| environment72 | - |
| environment73 | - |
| environment74 | - |
| environment75 | - |
| environment76 | - |
| environment77 | - |
| environment78 | - |
| environment79 | - |
| environment80 | - |

## Authorization

This API uses the following authentication schemes.

* [`thingspace_oauth (OAuth 2 Client Credentials Grant)`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/oauth-2-client-credentials-grant.md)
* [`VZ-M2M-Token (Custom Header Signature)`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/custom-header-signature.md)
* [`SessionToken (Custom Header Signature)`](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/auth/custom-header-signature-1.md)

## List of APIs

* [5 G Edge Platforms](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/5-g-edge-platforms.md)
* [Service Endpoints](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/service-endpoints.md)
* [Service Profiles](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/service-profiles.md)
* [Device Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-management.md)
* [Device Groups](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-groups.md)
* [Session Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/session-management.md)
* [Connectivity Callbacks](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/connectivity-callbacks.md)
* [Account Requests](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/account-requests.md)
* [Service Plans](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/service-plans.md)
* [Device Diagnostics](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-diagnostics.md)
* [Device Profile Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-profile-management.md)
* [Device Monitoring](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-monitoring.md)
* [E UICC Device Profile Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/e-uicc-device-profile-management.md)
* [Devices Locations](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/devices-locations.md)
* [Devices Location Subscriptions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/devices-location-subscriptions.md)
* [Device Location Callbacks](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-location-callbacks.md)
* [Usage Trigger Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/usage-trigger-management.md)
* [Software Management Subscriptions V1](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-subscriptions-v1.md)
* [Software Management Licenses V1](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-licenses-v1.md)
* [Firmware V1](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/firmware-v1.md)
* [Software Management Callbacks V1](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-callbacks-v1.md)
* [Software Management Reports V1](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-reports-v1.md)
* [Software Management Licenses V2](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-licenses-v2.md)
* [Campaigns V2](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/campaigns-v2.md)
* [Software Management Callbacks V2](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-callbacks-v2.md)
* [Software Management Reports V2](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-reports-v2.md)
* [Client Logging](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/client-logging.md)
* [Server Logging](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/server-logging.md)
* [Configuration Files](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/configuration-files.md)
* [Software Management Subscriptions V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-subscriptions-v3.md)
* [Software Management Licenses V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-licenses-v3.md)
* [Campaigns V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/campaigns-v3.md)
* [Software Management Reports V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-reports-v3.md)
* [Firmware V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/firmware-v3.md)
* [Account Devices](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/account-devices.md)
* [Software Management Callbacks V3](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/software-management-callbacks-v3.md)
* [SIM Securefor Io T Licenses](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sim-securefor-io-t-licenses.md)
* [Account Subscriptions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/account-subscriptions.md)
* [Performance Metrics](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/performance-metrics.md)
* [Diagnostics Subscriptions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-subscriptions.md)
* [Diagnostics Observations](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-observations.md)
* [Diagnostics History](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-history.md)
* [Diagnostics Settings](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-settings.md)
* [Diagnostics Callbacks](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-callbacks.md)
* [Diagnostics Factory Reset](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/diagnostics-factory-reset.md)
* [Cloud Connector Subscriptions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/cloud-connector-subscriptions.md)
* [Cloud Connector Devices](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/cloud-connector-devices.md)
* [Device Service Management](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-service-management.md)
* [Device Reports](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-reports.md)
* [Anomaly Settings](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/anomaly-settings.md)
* [Anomaly Triggers](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/anomaly-triggers.md)
* [Anomaly Triggers V2](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/anomaly-triggers-v2.md)
* [Wireless Network Performance](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/wireless-network-performance.md)
* [Fixed Wireless Qualification](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/fixed-wireless-qualification.md)
* [Managinge SIM Profiles](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/managinge-sim-profiles.md)
* [Device SMS Messaging](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-sms-messaging.md)
* [Device Actions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/device-actions.md)
* [Thing Space Qualityof Service API Actions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/thing-space-qualityof-service-api-actions.md)
* [Promotion Period Information](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/promotion-period-information.md)
* [Retrievethe Triggers](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/retrievethe-triggers.md)
* [SIM Actions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sim-actions.md)
* [App Config Service](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/app-config-service.md)
* [Map Data Manager](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/map-data-manager.md)
* [5 GBI Device Actions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/5-gbi-device-actions.md)
* [Sensor Insights Sensors](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-sensors.md)
* [Sensor Insights Devices](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-devices.md)
* [Sensor Insights Gateways](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-gateways.md)
* [Sensor Insights Smart Alerts](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-smart-alerts.md)
* [Sensor Insights Rules](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-rules.md)
* [Sensor Insights Health Score](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-health-score.md)
* [Sensor Insights Notification Groups](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-notification-groups.md)
* [Sensor Insights Users](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sensor-insights-users.md)
* [Accounts](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/accounts.md)
* [SMS](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/sms.md)
* [Exclusions](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/exclusions.md)
* [Billing](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/billing.md)
* [Targets](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/targets.md)
* [PWN](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/pwn.md)
* [Registration](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/controllers/registration.md)

## SDK Infrastructure

### HTTP

* [HttpResponse](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/http-response.md)
* [HttpRequest](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/http-request.md)

### Utilities

* [ApiHelper](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/api-helper.md)
* [HttpDateTime](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/http-date-time.md)
* [RFC3339DateTime](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/rfc3339-date-time.md)
* [UnixDateTime](https://www.github.com/rehanalam/vz-test-package-python-sdk/tree/20.20.10/doc/unix-date-time.md)

