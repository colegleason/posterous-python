# Copyright:
#    Copyright (c) 2010, Benjamin Reitzammer <http://github.com/nureineide>, 
#    All rights reserved.
#            
# License:
#    This program is free software. You can distribute/modify this program under
#    the terms of the Apache License Version 2.0 available at 
#    http://www.apache.org/licenses/LICENSE-2.0.txt 

import urllib.request, urllib.parse, urllib.error
from datetime import datetime
from base64 import b64encode

from posterous.utils import enc_utf8_str


def bind_method(**options):

    class APIMethod(object):
        # Get the options for the api method
        path = options['path']
        payload_type = options.get('payload_type', None)
        payload_list = options.get('payload_list', False)
        response_type = options.get('response_type', 'xml')
        allowed_param = options.get('allowed_param', [])
        method = options.get('method', 'GET')
        auth_type = options.get('auth_type', None)

        def __init__(self, api, args, kwargs):
            # If the method requires authentication and no credentials
            # are provided, throw an error.  If credentials are 
            # provided, get and API token.
            if self.auth_type == "basic" and not (api.username and api.password):
                raise Exception('Authentication is required!')
            elif self.auth_type == "token" and not (api.token):
                if not (api.username and api.password):
                    raise Exception('Authentication is required!')
                else:
                    self._get_api_token(api.username, api.password)

            self.api = api
            self.headers = kwargs.pop('headers', {})
            self.auth_url = api.auth_url
            self.api_url = api.host + api.api_root
            self._build_parameters(args, kwargs)

        def _get_api_token(self, username, password):
            url = self.api_url + '/' + self.auth_url
            auth = b64encode('{0}:{1}'.format(
                    self.api.username, 
                    self.api.password).encode('latin-1'))
            self.headers['Authorization'] = 'Basic %s'.format(auth)
            
        def _build_parameters(self, args, kwargs):
            self.parameters = []
            
            args = list(args)
            args.reverse()

            for name, p_type in self.allowed_param:
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
            url = self.api_url + '/' + self.path

            # Apply authentication if required
            if self.auth_type = "basic":
                auth = b64encode('{0}:{1}'.format(
                        self.api.username, 
                        self.api.password).encode('latin-1'))
                self.headers['Authorization'] = 'Basic %s'.format(auth)
            if self.auth_type = "token":
                self.headers['api_token'] = self.api.api_token
                
           
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

