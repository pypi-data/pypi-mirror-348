# -*- coding: utf-8 -*-
from chibi_requests import Chibi_url
from chibi_requests.response import Response as Response_base
from .soup import Chibi_soup


class Response( Response_base ):
    is_raise_when_no_ok = True

    def parse_like_html( self ):
        return Chibi_soup( self.body, 'html.parser' )


class Chibi_site( Chibi_url ):
    def __new__( cls, *args, **kw ):
        kw.setdefault( 'response_class', Response )
        obj = super().__new__( cls, *args, **kw )

        return obj

    @property
    def response( self ):
        try:
            return self._response
        except AttributeError:
            self._response = self.get()
            return self._response

    @property
    def soup( self ):
        return self.response.native

    @property
    def images( self ):
        return self.soup.select( 'img' )

    @property
    def sections( self ):
        return self.soup.select( 'section' )

    @property
    def articles( self ):
        return self.soup.select( 'article' )

    @property
    def links( self ):
        return self.soup.select( 'a' )

    @property
    def links_as_string( self ):
        return list( a.attrs[ 'href' ] for a in self.links )

    @property
    def urls( self ):
        klass = type( self )
        return list( klass( a.attrs[ 'href' ] ) for a in self.links )
