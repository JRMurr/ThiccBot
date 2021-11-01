# \ApikeyWordsApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_keyword**](ApikeyWordsApi.md#create_keyword) | **Post** /api/keyWords/{server_type}/{server_id} | Create a new KeyWord
[**delete_keyword**](ApikeyWordsApi.md#delete_keyword) | **Delete** /api/keyWords/{server_type}/{server_id}/{key_name} | 
[**get_keyword**](ApikeyWordsApi.md#get_keyword) | **Get** /api/keyWords/{server_type}/{server_id}/{key_name} | 
[**list_keywords**](ApikeyWordsApi.md#list_keywords) | **Get** /api/keyWords/{server_type}/{server_id} | 
[**update_keyword**](ApikeyWordsApi.md#update_keyword) | **Put** /api/keyWords/{server_type}/{server_id}/{key_name} | 


# **create_keyword**
> ::models::KeyWord create_keyword(server_id, server_type, payload, optional)
Create a new KeyWord

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**KeyWord**](KeyWord.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**KeyWord**](KeyWord.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::KeyWord**](KeyWord.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_keyword**
> delete_keyword(key_name, server_id, server_type)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **key_name** | **String**| The name of the key word | 
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

# **get_keyword**
> ::models::KeyWord get_keyword(key_name, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **key_name** | **String**| The name of the key word | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key_name** | **String**| The name of the key word | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::KeyWord**](KeyWord.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_keywords**
> ::models::KeyWord list_keywords(server_id, server_type, optional)


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

[**::models::KeyWord**](KeyWord.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_keyword**
> ::models::KeyWord update_keyword(key_name, server_id, server_type, payload, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **key_name** | **String**| The name of the key word | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**KeyWord**](KeyWord.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key_name** | **String**| The name of the key word | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**KeyWord**](KeyWord.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::KeyWord**](KeyWord.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

