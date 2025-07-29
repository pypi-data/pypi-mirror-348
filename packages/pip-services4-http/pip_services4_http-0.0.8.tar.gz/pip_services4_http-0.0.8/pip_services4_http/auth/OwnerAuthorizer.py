# -*- coding: utf-8 -*-
from typing import Callable

import bottle
from pip_services4_commons.errors import UnauthorizedException

from pip_services4_http.controller.HttpResponseSender import HttpResponseSender


class OwnerAuthorizer:

    def owner(self, id_param: str = 'user_id') -> Callable:
        def inner():
            user = bottle.request.environ.get('bottle.request.ext.user')
            if user is None:
                raise bottle.HTTPResponse(HttpResponseSender.send_error(UnauthorizedException(
                    None,
                    'NOT_SIGNED',
                    'User must be signed in to perform this operation'
                ).with_status(401)), status=401)
            else:
                user_id = dict(bottle.request.query.decode()).get(id_param)
                if bottle.request.user_id != user_id:
                    raise bottle.HTTPResponse(HttpResponseSender.send_error(UnauthorizedException(
                        None,
                        'FORBIDDEN',
                        'Only data owner can perform this operation'
                    ).with_status(403)), status=403)

        return inner

    def owner_or_admin(self, id_param: str = 'user_id') -> Callable:
        def inner():
            user = bottle.request.environ.get('bottle.request.ext.user')
            if user is None:
                raise bottle.HTTPResponse(HttpResponseSender.send_error(UnauthorizedException(
                    None,
                    'NOT_SIGNED',
                    'User must be signed in to perform this operation'
                ).with_status(401)), status=401)
            else:
                user_id = dict(bottle.request.query.decode()).get(id_param)
                if hasattr(bottle.request, 'user'):
                    roles = bottle.request.user.roles
                else:
                    roles = None
                admin = 'admin' in roles
                if user != user_id and not admin:
                    raise bottle.HTTPResponse(HttpResponseSender.send_error(UnauthorizedException(
                        None,
                        'FORBIDDEN',
                        'Only data owner can perform this operation'
                    ).with_status(403)), status=403)

        return inner
