def dpath(dikt):
    """Helper to create a DPath that is nice to read e.g. dpath(my_dict)['a', 'b']

    :param dikt: Dictionary to wrap in DPath
    :return: A DPath object
    """
    return DPath(dikt)

class DPath:
    """dpath is a tool for navigating multidimensional map structures easily

    >>> from pprint import pprint  # for consistency of dict assert
    >>> my_dict = {'eggs': {'ham': 4, 'bacon': {23: 3}}, ('cheese',): 666, 'cheese': 42}
    >>> x = dpath(my_dict)
    >>> x['foo']
    >>> x['eggs', 'bacon', 23, 'bar']
    >>> x[('ham',)]
    >>> x[('cheese',)]
    666
    >>> x['cheese']
    42
    >>> x['eggs', 'ham']
    4
    >>> x['eggs', 'bacon', 23]
    3
    >>> pprint(x['eggs', 'bacon'])
    {23: 3}
    >>> pprint(x['eggs'])
    {'bacon': {23: 3}, 'ham': 4}
    >>> pprint(x.unwrap())
    {'cheese': 42, 'eggs': {'bacon': {23: 3}, 'ham': 4}, ('cheese',): 666}
    """

    def __init__(self, dikt):
        if not isinstance(dikt, dict):
            raise ValueError('Wrong type: {0}, need dict'.format(type(dikt)))
        self.dikt = dikt

    def unwrap(self):
        return self.dikt

    def __getitem__(self, *args):
        # Make args consistently iterable if 1 or many passed
        # Also handle weird case when single key is used that is a single element tuple
        # e.g. dpath({'eggs': 2, ('eggs',): 3})['eggs'] -> 2 or 3?
        if isinstance(args[0], tuple) and len(args[0]) > 1:
            path = args[0]
        else:
            path = args

        # Try to follow path until we can't
        node = self.dikt
        for path_elem in path:
            # Can't continue because trying to follow path into non-dict
            if type(node) is not dict:
                return None
            # Can't continue because no key matching path elem
            if path_elem not in node:
                return None
            node = node[path_elem]
        return node

    def __setitem__(self, *path):
        raise NotImplementedError('Coming soon...')
