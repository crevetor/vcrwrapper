import os
from functools import wraps
from django.conf import settings
from . import vcrutils
from .utils import dual_decorator
 
VCR_CASSETTE_PATH = settings.VCR_CASSETTE_PATH
MAKE_EXTERNAL_REQUESTS = os.environ.get('MAKE_EXTERNAL_REQUESTS') == 'TRUE'
 
 
@dual_decorator  # convert a paramaterized decorator for no-arg use (https://gist.github.com/simon-weber/9956622).
def external_call(*args, **kwargs):
    """Enable vcrpy to store/mock http requests.

    The most basic use looks like::
        @external_call
        def test_foo(self):
            # urllib2, urllib3, and requests will be recorded/mocked.
            ...

    By default, the matching strategy is very restrictive.
    To customize it, this decorator's params are passed to vcr.VCR().
    For example, to customize the matching strategy, do::
        @external_call(match_on=['url', 'host'])
        def test_foo(self):
            ...

    If it's easier to match requests by introducing subcassettes,
    the decorator can provide a context manager::
        @external_call(use_namespaces=True)
        def test_foo(self, vcr_namespace):  # this argument must be present
            # do some work with the base cassette
            with vcr_namespace('do_other_work'):
                # this uses a separate cassette namespaced under the parent

            # we're now using the base cassette again

    To force decorated tests to make external requests, set
    the MAKE_EXTERNAL_REQUESTS envvar to TRUE.

    Class method tests are also supported.
    """
 
    use_namespaces = kwargs.pop('use_namespaces', False)
 
    vcr_args = args
    vcr_kwargs = kwargs
 
    default_vcr_kwargs = {
        'cassette_library_dir': VCR_CASSETTE_PATH,
        'record_mode': 'none',
        'match_on': ('method', 'scheme', 'host', 'port', 'path', 'query'),
        'filter_headers': ['authorization']
    }
 
    default_vcr_kwargs.update(vcr_kwargs)
 
    match_on = default_vcr_kwargs.pop('match_on')
 
    def decorator(f, vcr_args=vcr_args, vcr_kwargs=default_vcr_kwargs,
                  match_on=match_on, use_namespaces=use_namespaces):
 
        # this is used as a nose attribute:
        #  http://nose.readthedocs.org/en/latest/plugins/attrib.html
        f.external_api = True
 
        @wraps(f)
        def wrapper(*args, **kwargs):
            my_vcr = vcrutils.get_vcr(*vcr_args, **vcr_kwargs)
            cassette_filename = vcrutils.get_filename_from_method(f, args[0])
 
            if use_namespaces:
                kwargs['vcr_namespace'] = vcrutils.get_namespace_cm(
                    my_vcr, cassette_filename, MAKE_EXTERNAL_REQUESTS)
 
            if MAKE_EXTERNAL_REQUESTS:
                return f(*args, **kwargs)
            else:
                with my_vcr.use_cassette(cassette_filename, match_on=match_on):
                    return f(*args, **kwargs)
        return wrapper
    return decorator
