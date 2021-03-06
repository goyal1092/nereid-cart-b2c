# -*- coding: UTF-8 -*-
'''
    nereid_cart.sale

    Sales modules changes to fit nereid

    :copyright: (c) 2010-2014 by Openlabs Technologies & Consulting (P) Ltd.
    :license: GPLv3, see LICENSE for more details
'''
from trytond.pool import PoolMeta
from trytond.model import fields
from nereid import request, current_user
from nereid.ctx import has_request_context

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    '''Add a boolean to indicate if the order originated from a shopping cart.
    '''
    __name__ = 'sale.sale'

    is_cart = fields.Boolean(
        'Is Cart Order?', readonly=True, select=True
    )
    website = fields.Many2One(
        'nereid.website', 'Website', readonly=True, select=True
    )
    nereid_user = fields.Many2One(
        'nereid.user', 'Nereid User', select=True
    )

    @staticmethod
    def default_is_cart():
        """Dont make this as a default as this would cause orders being placed
        from backend to be placed under default.
        """
        return False

    @staticmethod
    def default_price_list(user=None):
        """Get the pricelist of active user. In the
        event that the logged in user does not have a pricelist set against
        the user, the guest user's pricelist is chosen.

        :param user: active record of the nereid user
        """
        if not has_request_context():
            # Not a nereid request
            return None

        if user is not None and user.party.sale_price_list:
            # If a user was provided and the user has a pricelist, use
            # that
            return user.party.sale_price_list.id

        if not current_user.is_anonymous() and \
                current_user.party.sale_price_list:
            # If the currently logged in user has a pricelist defined, use
            # that
            return current_user.party.sale_price_list.id

        # Since there is no pricelist for the user, use the guest user's
        # pricelist if one is defined.
        guest_user = request.nereid_website.guest_user
        if guest_user.party.sale_price_list:
            return guest_user.party.sale_price_list.id

        return None
