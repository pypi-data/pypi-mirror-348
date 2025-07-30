from chibi.file import Chibi_file
from .soup import Chibi_soup


__all__ = [ 'Chibi_file_html' ]


class Chibi_file_html( Chibi_file ):
    """
    chibi file para leer htmls
    """
    def read( self ):
        """
        lee archivos como htmls

        Returns
        -------
        chibi_site.soup.Chibi_soup
        """
        data = super().read()
        return Chibi_soup( data, 'html.parser' )

    def write( self, data ):
        raise NotImplementedError
