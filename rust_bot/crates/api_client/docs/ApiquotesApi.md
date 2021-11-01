# \ApiquotesApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_quote**](ApiquotesApi.md#create_quote) | **Post** /api/quotes/{server_type}/{server_id} | Create a new Quote
[**delete_quote**](ApiquotesApi.md#delete_quote) | **Delete** /api/quotes/{server_type}/{server_id}/{quote_id} | 
[**get_quote**](ApiquotesApi.md#get_quote) | **Get** /api/quotes/{server_type}/{server_id}/{quote_id} | 
[**get_random_quote**](ApiquotesApi.md#get_random_quote) | **Get** /api/quotes/{server_type}/{server_id}/random | 
[**list_quotes**](ApiquotesApi.md#list_quotes) | **Get** /api/quotes/{server_type}/{server_id} | 


# **create_quote**
> ::models::Quote create_quote(server_id, server_type, payload, optional)
Create a new Quote

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The server type (discord, irc, etc) | 
  **payload** | [**Quote**](Quote.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The server type (discord, irc, etc) | 
 **payload** | [**Quote**](Quote.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Quote**](quote.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_quote**
> delete_quote(quote_id, server_id, server_type)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **quote_id** | **i32**| The id of the quote | 
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

# **get_quote**
> ::models::Quote get_quote(quote_id, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **quote_id** | **i32**| The id of the quote | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **quote_id** | **i32**| The id of the quote | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Quote**](quote.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_random_quote**
> ::models::Quote get_random_quote(server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The server type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The server type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Quote**](quote.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_quotes**
> ::models::Quote list_quotes(server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The server type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The server type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Quote**](quote.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

