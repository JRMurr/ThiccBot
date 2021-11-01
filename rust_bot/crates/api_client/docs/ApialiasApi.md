# \ApialiasApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_alias**](ApialiasApi.md#create_alias) | **Post** /api/alias/{server_type}/{server_id} | Create a new Alias
[**delete_alias**](ApialiasApi.md#delete_alias) | **Delete** /api/alias/{server_type}/{server_id}/{alias_name} | 
[**get_alias**](ApialiasApi.md#get_alias) | **Get** /api/alias/{server_type}/{server_id}/{alias_name} | 
[**list_aliases**](ApialiasApi.md#list_aliases) | **Get** /api/alias/{server_type}/{server_id} | 
[**update_alias**](ApialiasApi.md#update_alias) | **Put** /api/alias/{server_type}/{server_id}/{alias_name} | 


# **create_alias**
> ::models::Alias create_alias(server_id, server_type, payload, optional)
Create a new Alias

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**Alias**](Alias.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**Alias**](Alias.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Alias**](Alias.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_alias**
> delete_alias(alias_name, server_id, server_type)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **alias_name** | **String**| The name of the alias | 
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

# **get_alias**
> ::models::Alias get_alias(alias_name, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **alias_name** | **String**| The name of the alias | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alias_name** | **String**| The name of the alias | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Alias**](Alias.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_aliases**
> ::models::Alias list_aliases(server_id, server_type, optional)


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

[**::models::Alias**](Alias.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_alias**
> ::models::Alias update_alias(alias_name, server_id, server_type, payload, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **alias_name** | **String**| The name of the alias | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**Alias**](Alias.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **alias_name** | **String**| The name of the alias | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**Alias**](Alias.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Alias**](Alias.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

