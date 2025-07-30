from chibi.file import Chibi_file
from .soup import Chibi_soup


__all__ = [ 'Chibi_file_html' ]


class Chibi_file_html( Chibi_file ):
    def read( self ):
        data = super().read()
        return Chibi_soup( data, 'html.parser' )

    def write( self, data ):
        raise NotImplementedError
