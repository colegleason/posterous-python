from postypy.bind import bind_method

class PostyAPI(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.host = 'http://posterous.com'
        self.api_root = "/api/2"
    
    ### Posterous API calls
    """
    * Required Arguments
    "path" - The path for the api call.
    * Optional Arguments
    "method" - GET (defualt), POST, or DELETE
    "response_type" - The model to use when parsing.
    "auth_type" - The type of authentication used.  It can be either None
        (default), "basic", or "token".
    "parameters" - The parameters that may be supplied to the call as
        documented on apidocs.posterous.com
        -- "user_id" - "me" by default 
    """
    ## Authentication
    
    ''' Returns the API token for the username and password supplied with
    the API call.  This does not need to be explicitly called to use other
    methods that require token authorization.'''
    get_api_token = bind_method(
        path = '/auth/token',
        response_type = 'token',
        auth_type = 'basic',
        parameters = []
        )
    ## Sites
    
    ''' Returns a list of Site objects for all sites owned by the user.'''
    get_sites = bind_method(
        path = '/users/{user_id}/sites',
        response_type = 'site_list',
        auth_type = 'token',
        parameters = [
            ('user_id', str)]
        )
    
    ''' Gets a single site and returns it as a Site object.'''
    get_site = bind_method(
        path = '/users/{user_id}/sites',
        response_type = 'site',
        auth_type = 'token',
        parameters = [
            ('user_id', str),
            ('hostname', str)]
        )
        
    ''' Returns a single Site object for the user's primary site. '''
    get_primary_site = bind_method(
        path = 'users/{user_id}/sites/primary',
        response_type = 'site',
        auth_type = 'token',
        parameters = [
            ('user_id', str)]
        )
        
    ''' Creates a new Posterous site and returns that site as a Site object.'''
    create_site = bind_method(
        path = '/users/{user_id}/sites',
        method = 'POST',
        response_type = 'site',
        auth_type = 'token',
        parameters = [
            ('user_id', str),
            ('name', str),
            ('is_private', bool),
            ('hostname', str)]
        )
    
    ''' Deletes a single site and returns a HTTP 200 OK status.'''
    delete_site = bind_method(
        path = '/users/{user_id}/sites',
        method = 'DELETE',
        response_type = 'ok_code',
        auth_type = 'token',
        parameters = [
            ('user_id', str),
            ('hostname', str)]
        )
        
    ''' Get a site's subscribers.'''
    delete_site = bind_method(
        path = '/users/{user_id}/sites',
        method = 'DELETE',
        response_type = 'ok_code',
        auth_type = 'token',
        parameters = [
            ('user_id', str),
            ('hostname', str)]
        )
    