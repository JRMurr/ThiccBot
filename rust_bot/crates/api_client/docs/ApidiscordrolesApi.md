# \ApidiscordrolesApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_role**](ApidiscordrolesApi.md#create_role) | **Post** /api/discord/roles/{server_id} | Create a new role message listener
[**delete_role**](ApidiscordrolesApi.md#delete_role) | **Delete** /api/discord/roles/{id} | 
[**list_roles**](ApidiscordrolesApi.md#list_roles) | **Get** /api/discord/roles/{server_id} | 


# **create_role**
> ::models::Role create_role(server_id, payload, optional)
Create a new role message listener

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the discord server | 
  **payload** | [**Role**](Role.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the discord server | 
 **payload** | [**Role**](Role.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Role**](role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role**
> ::models::Role delete_role(id, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **id** | **i32**| The id for the role object | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **i32**| The id for the role object | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Role**](role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_roles**
> ::models::Role list_roles(server_id, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the discord server | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the discord server | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Role**](role.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

