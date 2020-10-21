import re
import sys
import logging

from typing import Optional

#logger = logging.getLogger("doi")   # type: logging.Logger
logging.basicConfig(filename='doi.log',level=logging.DEBUG)
logging.info('Started')


#https://github.com/papis/python-doi/blob/master/src/doi/__init__.py
def validate_doi(doi: str) -> Optional[str]:
    """We check that the DOI can be resolved by
    `official means <http://www.doi.org/factsheets/DOIProxy.html>`_. If so, we
    return the resolved URL, otherwise, we return ``None`` (which means the
    DOI is invalid).
    :param doi: Identifier.
    :returns: The URL assigned to the DOI or ``None``.
    """
    from urllib.error import HTTPError
    import urllib.request
    import urllib.parse
    import json
    url = "https://doi.org/api/handles/{doi}".format(doi=doi)
    #logging.debug('handle url %s', url)
    request = urllib.request.Request(url)

    try:
        result = json.loads(urllib.request.urlopen(request).read().decode())
    except HTTPError:
        #logging.debug(str(url), ' HTTP 404: DOI not found')
        raise ValueError('HTTP 404: DOI not found')
    else:
        urls = [v['data']['value']
                for v in result['values'] if v.get('type') == 'URL']
        if urls:
            logging.debug("['" + doi + "']:['" + urls[0] + "','" + url + "']")
        else:
            logging.debug("None")
        
        return urls[0] if urls else None