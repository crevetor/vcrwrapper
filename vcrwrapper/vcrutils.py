from contextlib import contextmanager
import inspect
 
import vcr
 
def get_vcr(*args, **kwargs):
    """Return a VCR, with our custom matchers registered.

    Params are passed to VCR init."""
 
    v = vcr.VCR(*args, **kwargs)
    # register custom matchers here
 
    return v
 
 
def get_filename_from_method(func, receiver):
    """Return an unambigious filename built from a test method invocation.

    The method is assumed to be declared inside venmo_tests.

    :attr func: the method's function object.
    :attr receiver: the first argument to the method, i.e. self or cls.
    """
 
    mod_name = func.__module__
 
    if inspect.isclass(receiver):
        class_name = receiver.__name__
    else:
        class_name = receiver.__class__.__name__
 
    return "%s.%s.%s.yaml" % (mod_name, class_name, func.__name__)
 
 
def _get_subcassette_filename(name, parent_filename):
    """Return a cassette namespaced by a parent cassette filename.

    For example::
        >>> _get_subcassette_filename('foo', 'mytests.test_bar.yaml')
        'mytests.test_bar.foo.yaml'
    """
    parent_components = parent_filename.split('.')
    parent_components.insert(len(parent_components) - 1, name)
 
    return '.'.join(parent_components)
 
 
def get_namespace_cm(my_vcr, parent_filename, make_external_requests):
    """Return a context manager that uses a cassette namespaced under the parent.

    The context manager takes two arguments:
        * name: a string that names the cassette.
        * match_on: (optional), passed to use_cassette to override the default.
    """
    @contextmanager
    def namespace_cm(name, match_on=None,
                     my_vr=my_vcr, parent_filename=parent_filename,
                     make_external_requests=make_external_requests):
        if make_external_requests:
            yield
        else:
            kwargs = {
                'path': _get_subcassette_filename(name, parent_filename),
                'match_on': match_on
            }
 
            if match_on is None:
                # vcr doesn't use a sentinel for match_on;
                # it just shouldn't be present to default it.
                del kwargs['match_on']
 
            with my_vcr.use_cassette(**kwargs):
                yield
 
    return namespace_cm
