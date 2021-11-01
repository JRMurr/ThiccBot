# \ApialbumsApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_album_entry**](ApialbumsApi.md#add_album_entry) | **Delete** /api/albums/{server_type}/{server_id}/entry/{entry_id} | 
[**add_album_entry_0**](ApialbumsApi.md#add_album_entry_0) | **Post** /api/albums/{server_type}/{server_id}/{album_name}/entries | 
[**create_album**](ApialbumsApi.md#create_album) | **Post** /api/albums/{server_type}/{server_id} | Create a new Album
[**delete_album**](ApialbumsApi.md#delete_album) | **Delete** /api/albums/{server_type}/{server_id}/{album_name} | 
[**get_album**](ApialbumsApi.md#get_album) | **Get** /api/albums/{server_type}/{server_id}/{album_name} | 
[**get_album_entries**](ApialbumsApi.md#get_album_entries) | **Get** /api/albums/{server_type}/{server_id}/{album_name}/entries | 
[**list_albums**](ApialbumsApi.md#list_albums) | **Get** /api/albums/{server_type}/{server_id} | List all albums on this server


# **add_album_entry**
> ::models::AlbumEntry add_album_entry(entry_id, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **entry_id** | **String**| The Id of the entry | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entry_id** | **String**| The Id of the entry | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::AlbumEntry**](albumEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_album_entry_0**
> ::models::AlbumEntry add_album_entry_0(server_id, server_type, album_name, payload, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **album_name** | **String**|  | 
  **payload** | [**AlbumEntry**](AlbumEntry.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **album_name** | **String**|  | 
 **payload** | [**AlbumEntry**](AlbumEntry.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::AlbumEntry**](albumEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_album**
> ::models::Album create_album(server_id, server_type, payload, optional)
Create a new Album

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **payload** | [**Album**](Album.md)|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **payload** | [**Album**](Album.md)|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Album**](album.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_album**
> delete_album(album_name, server_id, server_type)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **album_name** | **String**| The name of the album | 
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

# **get_album**
> ::models::Album get_album(album_name, server_id, server_type, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **album_name** | **String**| The name of the album | 
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **album_name** | **String**| The name of the album | 
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::Album**](album.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_album_entries**
> ::models::AlbumEntry get_album_entries(server_id, server_type, album_name, optional)


### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
  **server_id** | **i32**| The id of the server | 
  **server_type** | **String**| The sever type (discord, irc, etc) | 
  **album_name** | **String**|  | 
 **optional** | **map[string]interface{}** | optional parameters | nil if no parameters

### Optional Parameters
Optional parameters are passed through a map[string]interface{}.

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **server_id** | **i32**| The id of the server | 
 **server_type** | **String**| The sever type (discord, irc, etc) | 
 **album_name** | **String**|  | 
 **x_fields** | **String**| An optional fields mask | 

### Return type

[**::models::AlbumEntry**](albumEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_albums**
> ::models::Album list_albums(server_id, server_type, optional)
List all albums on this server

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

[**::models::Album**](album.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

