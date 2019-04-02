from flask import jsonify, request
from werkzeug.urls import Href


def paged_response(query, serialize_fn, default_size=20, maximum_size=100):
    """
    Paginate a query and generate a response object.

    :param query: A SQLAlchemy query object
    :param serialize_fn: A callable responsible for serializing the response
    :param default_size: The default page size if none is provided in the request
    :param maximum_size: The maximum page size allowed
    """
    href = Href(request.base_url)
    args = dict(request.args)

    # insert the page size parameter if not provided in the args
    args['per_page'] = args.get('per_page', None)

    page = query.paginate()

    response = jsonify(serialize_fn(page.items))
    links = []

    # generate link header
    args['page'] = 1
    links.append('<%s>; rel="first"' % href(**args))

    args['page'] = max(1, page.pages)
    links.append('<%s>; rel="last"' % href(**args))

    if page.has_prev:
        args['page'] = page.prev_num
        links.append('<%s>; rel="prev"' % href(**args))

    if page.has_next:
        args['page'] = page.next_num
        links.append('<%s>; rel="next"' % href(**args))

    response.headers['Link'] = ', '.join(links)
    response.headers['Resource-Count'] = query.count()
    response.headers['Page-Count'] = page.pages
    return response
