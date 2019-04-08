from flask import abort, jsonify, request
from marshmallow import fields, validate
from werkzeug.urls import Href


pagination_args = {
    'limit': fields.Int(missing=20, validate=validate.Range(min=1)),
    'offset': fields.Int(missing=0, validate=validate.Range(min=0))
}


def paged_response(query, args, serialize_fn, maximum_limit=None):
    """
    Paginate a query and generate a response object.

    :param query: A SQLAlchemy query object
    :param serialize_fn: A callable responsible for serializing the response
    :param args: Parsed request arguments
    :param maximum_limit: The maximum page size allowed
    """
    # We don't use the paginate() method from flask-sqlalchemy because it
    # does not allow the more flexible limit/offset api.
    limit = args['limit']
    offset = args['offset']
    total = query.count()
    href = Href(request.base_url)

    if offset > 0 and offset >= total:
        # This is the behavior of flask-sqlalchemy pagination, but we could instead
        # return an empty list.
        abort(404)

    if maximum_limit and limit > maximum_limit:
        # throw a validation error if the limit is larger than the maximum
        limit = validate.Range(min=1, max=maximum_limit)(limit)

    response = jsonify(serialize_fn(query.limit(limit).offset(offset)))
    response.headers['Resource-Count'] = total

    # generate link header
    links = []
    first_page = dict(args, limit=limit, offset=0)
    links.append('<%s>; rel="first"' % href(**first_page))

    last_page = dict(args, limit=limit, offset=max(0, limit * ((total - 1) // limit)))
    links.append('<%s>; rel="last"' % href(**last_page))

    if offset - limit >= 0:
        previous_page = dict(args, limit=limit, offset=(offset - limit))
        links.append('<%s>; rel="prev"' % href(**previous_page))

    if offset + limit < total:
        next_page = dict(args, limit=limit, offset=(offset + limit))
        links.append('<%s>; rel="next"' % href(**next_page))

    response.headers['Link'] = ', '.join(links)
    return response
