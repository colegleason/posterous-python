def bind_method(**options):
    
    
    class APIMethod(object):
        # Required arguments
        path = options['path']
        # Optional arguments
        method = options.get('method', 'GET')
        response_type = options.get('response_type', None)
        auth_type = options.get('auth_type', None)
        allowed_params = options.get('parameters', [])
        
        def __init__(self, api, args, kwargs):
            self.api = api
            self.headers = kwargs['headers']
            _check_authentication(api, auth_type)
            _check_params(args, kwargs)
            
        def _check_authentication(self, api, auth_type):
            if auth_type == None:
                pass
            elif auth_type == 'basic':
                if not (api.username and api.password):
                    raise Exception("You must suppy a username and password!")
                else:
                    creds = '{0}:{1}'.format(self.api.username, self.api.password)
                    auth = b64encode(creds.encode('latin-1'))
                    self.headers['Authorization'] = 'Basic %s'.format(auth)
            elif api_type = 'token':
                if api.api_token:
                    self.parameters['api_token'] = api.api_token
                elif not api.api_token and (self.api.username and self.api.password):
                    api.auth_token = api.get_api_token()
                else:
                    raise Exception("You must suppy a username and password!")
            else:
                raise Exception("Not a valid authentication type.")
                
        def _build_parameters(self, args, kwargs):
            self.parameters = []
            
            args = list(args)
            args.reverse()

            for name, p_type in self.allowed_params:
                value = None
                if args:
                    value = args.pop()

                if name in kwargs:
                    if not value:
                        value = kwargs.pop(name)
                    else:
                        raise TypeError('Multiple values for parameter {0} supplied!'.format(name))
                if not value:
                    continue

                if not isinstance(p_type, tuple):
                    p_type = (p_type,)

                self._check_type(value, p_type, name)
                self._set_param(name, value)
            
        def _check_type(self, value, p_type, name):
            """
            Throws a TypeError exception if the value type is not in the p_type tuple.
            """
            if not isinstance(value, p_type):
                raise TypeError('The value passed for parameter {0} is not valid! It must be one of these: {1}'.format(name, p_type))

            if isinstance(value, list):
                for val in value:
                    if isinstance(val, list) or not isinstance(val, p_type):
                        raise TypeError('A value passed for parameter {0} is not valid. It must be one of these: {1}'.format(name, p_type))
            
        def _set_param(self, name, value):
            """Do appropriate type casts and utf-8 encode the parameter values"""
            if isinstance(value, bool):
                value = int(value)
            
            elif isinstance(value, datetime):
                value = '{0} +0000'.format(value.strftime('%a, %d %b %Y %H:%M:%S').split('.')[0])
            
            elif isinstance(value, list):
                for val in value:
                    self.parameters.append(('{0}[]'.format(name), enc_utf8_str(val)))
                return

            self.parameters.append((name, enc_utf8_str(value)))

        def execute(self):
            # Build request URL
            url = self.api_url + self.path

            # Apply authentication if required
            if self.auth_type = "basic":
                auth = b64encode('{0}:{1}'.format(
                        self.api.username, 
                        self.api.password).encode('latin-1'))
                self.headers['Authorization'] = 'Basic %s'.format(auth)
            if self.auth_type = "token":
                self.parameters['api_token'] = self.api.api_token
                
            # Encode the parameters
            post_data = None
            if self.method == 'POST':
                post_data = urllib.parse.urlencode(self.parameters)
            elif self.method == 'GET' and self.parameters:
                url = '{0}?{1}'.format(url, urllib.parse.urlencode(self.parameters))
            
            # Make the request
            try:
                request = urllib.request.Request(url, post_data, self.headers)
                resp = urllib.request.urlopen(request)
            except Exception as e:
                # TODO: do better parsing of errors
                raise Exception('Failed to send request: {0}'.format(e))

            return self.api.parser.parse(self, resp.read())

    
    def _call(api, *args, **kwargs):
        method = APIMethod(api, args, kwargs)
        return method.execute()

    return _call

            