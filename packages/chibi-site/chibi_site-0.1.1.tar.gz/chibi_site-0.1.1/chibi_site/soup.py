from chibi.file.temp import Chibi_temp_path
from chibi_site.path import Chibi_path_browser
from bs4 import BeautifulSoup, ResultSet, CSS, Tag


class Chibi_result_set( ResultSet ):
    def to_html( self, path=None, to_temp=True ):
        if not path:
            path = Chibi_temp_path( delete_on_del=False )
            html_file = Chibi_path_browser(
                path.temp_file( extension='html' ) )
        elems_str = "\n".join( i.prettify() for i in self )
        html = r"<html><body>" + elems_str + r"</body></html>"
        soup = BeautifulSoup( html , "html.parser" )
        soup_str = soup.prettify()
        html_file.open().write( soup_str )
        return html_file


class Chibi_css( CSS ):
    def _rs( self, results ):
        """Normalize a list of results to a py:class:`ResultSet`.

        A py:class:`ResultSet` is more consistent with the rest of
        Beautiful Soup's API, and :py:meth:`ResultSet.__getattr__` has
        a helpful error message if you try to treat a list of results
        as a single result (a common mistake).
        """
        return Chibi_result_set( None, results )


class Chibi_soup( BeautifulSoup ):
    """
    fecade para BeautifulSoup agrega que los results de css select
    puedan tener la funcion to_html para verlo en un archivo
    """
    def to_html( self ):
        raise NotImplementedError

    @property
    def css(self) -> CSS:
        """Return an interface to the CSS selector API."""
        return Chibi_css( self )
