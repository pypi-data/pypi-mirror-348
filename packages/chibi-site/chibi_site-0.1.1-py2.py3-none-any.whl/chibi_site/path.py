from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from chibi.file import Chibi_path
import logging


logger = logging.getLogger( 'chibi_site.path' )


class Chibi_path_browser( Chibi_path ):
    @property
    def browser( self ):
        try:
            return self._browser
        except AttributeError:
            logger.info( "abriendo navegador firefox" )
            options = self._build_firefox_options()
            self._browser = webdriver.Firefox( options=options )
            return self._browser

    def _build_firefox_options( self ):
        options = Options()
        options.headless = True
        return options

    def open_on_browser( self ):
        self.browser.get( 'file://' + str( self ) )

    def __del__( self ):
        if hasattr( self, '_browser' ):
            logger.info( "cerrando el navegador" )
            self.browser.quit()

