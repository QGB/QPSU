#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from _ast import AST
import ast
import json

import webapp2


class MainHandler( webapp2.RequestHandler ):

    def post( self ):
        node = ast.parse( self.request.get( 'pysrc' ) )

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write( ast2json( node ) )



def ast2json( node ):

    if not isinstance( node, AST ):
        raise TypeError( 'expected AST, got %r' % node.__class__.__name__ )


    def _format( node ):
        if isinstance( node, AST ):
            fields = [ ( '_PyType', _format( node.__class__.__name__ ) ) ]
            fields += [ ( a, _format( b ) ) for a, b in iter_fields( node ) ]

            return '{ %s }' % ', '.join( ( '"%s": %s' % field for field in fields ) )

        if isinstance( node, list ):
            return '[ %s ]' % ', '.join( [ _format( x ) for x in node ] )

        return json.dumps( node )


    return _format( node )



def iter_fields( node ):

    for field in node._fields:
        try:
            yield field, getattr( node, field )
        except AttributeError:
            pass



app = webapp2.WSGIApplication( [
    ( '/ast2json', MainHandler )
], debug=True )
