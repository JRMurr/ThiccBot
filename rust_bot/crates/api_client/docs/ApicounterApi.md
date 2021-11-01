# \ApicounterApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_counter**](ApicounterApi.md#create_counter) | **Post** /api/counter/{server_type}/{server_id} | Create a new Counter
[**delete_counter**](ApicounterApi.md#delete_counter) | **Delete** /api/counter/{server_type}/{server_id}/{counter_name} | 
[**get_counter**](ApicounterApi.md#get_counter) | **Get** /api/counter/{server_type}/{server_id}/{counter_name} | 
[**list_counter**](ApicounterApi.md#list_counter) | **Get** /api/counter/{server_type}/{server_id} | 
[**update_counter**](ApicounterApi.md#update_counter) | **Put** /api/counter/{server_type}/{server_id}/{counter_name} | 


# **create_counter**
> ::models::Counter create_counter(server_id, server_type, payload, optional)
Create a new Counter

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**Counter**](Counter.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**Counter**](Counter.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Counter**](Counter.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_counter**
> delete_counter(counter_name, server_id, server_type)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **counter_name** | **String**| The name of the counter | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 

### Return type

 (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_counter**
> ::models::Counter get_counter(counter_name, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **counter_name** | **String**| The name of the counter | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **counter_name** | **String**| The name of the counter | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Counter**](Counter.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_counter**
> ::models::Counter list_counter(server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Counter**](Counter.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_counter**
> ::models::Counter update_counter(counter_name, server_id, server_type, payload, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **counter_name** | **String**| The name of the counter | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**Counter**](Counter.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **counter_name** | **String**| The name of the counter | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**Counter**](Counter.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Counter**](Counter.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

