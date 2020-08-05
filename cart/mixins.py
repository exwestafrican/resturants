from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.shortcuts import render
from django.db.models import Q


class CreateCartMixin:
    """
    if auth user logs in and creates cart. check if current session_id belongs to user
    if not, check if user has an active cart.
    else create new session and cart.

    if anon user has session_id, check if session has a cart
    else create new cart for user
    """

    cart_serializer = CartSerializer

    def get_cart_queryset(self):
        """
        method retrives active cart via user if authenticated
        or session_id and cart_id stored in session_id.
        see models for definition of active cart.
        """
        # check if user is anonymous
        if self.request.session.session_key and not self.request.user.is_authenticated:
            # even authenticated users have session_ids
            queryset = Cart.objects.filter(
                session_id=self.request.session.session_key,
                cart_id=self.request.session.get("cart_id"),
                active=True,
            )
            # return an active cart i.e user is still shoping

        # user is logged in and has session_id
        elif self.request.user.is_authenticated and self.request.session.session_key:
            # check if autheticated user has an anonymous cart -
            # user might have gotten logged out, and wants to log back in immediately
            # if another user logs in after, new session gets created
            if self.request.session.get("user_id") is None:
                # if no user owns session, then sesion belongs to loged in user
                queryset = Cart.objects.filter(
                    Q(owner=self.request.user, active=True)
                    | Q(session_id=self.request.session.session_key, active=True)
                )

            else:
                # anonymous session might belong to another user
                queryset = Cart.objects.filter(owner=self.request.user, active=True)

        # user is authenticated with no session_id
        elif self.request.user.is_authenticated:
            queryset = Cart.objects.filter(owner=self.request.user, active=True)

        else:
            # i don't even think this is necessary
            queryset = []

        return queryset

    def does_browser_accepts_cookies(self):
        # test that user accepts cookies
        self.request.session.set_test_cookie()
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()  # good practise to delete test cookies
            # if i'm here, it means user accepts cookies, create session for user.
            self.request.session.create()
            return True
        else:
            return False

    def create_new_cart(self, request, *args, **kwargs):
        """
        decdies how to create a cart.
        """
        data = {}
        data["csrfmiddlewaretoken"] = request.data.get("csrfmiddlewaretoken")
        # cart doesn't need any data to get created but csrf is important for security.
        serializer = self.cart_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            content = self.perform_create_for_authenticated_user(serializer)
        # check if user has session
        elif request.session.session_key:

            content = self.perform_create_for_anonymous_user_with_session_id(serializer)
        # then just create a session id for user
        else:
            content = self.perform_create_for_anonymous_user_without_session_id(
                serializer
            )
        print("content", content)
        return content

    def perform_create_for_authenticated_user(self, serializer):
        """
        checks if autheticated user doesn't have an anonymous active cart
        creates cart for autenticated user
        sets session_id or sets to None 
        saves cart_ID in session_id 
        """

        # check if user's session has an active cart
        # and if the session belongs to the request user . assign cart session to request user
        if (
            Cart.objects.filter(
                session_id=self.request.session.session_key, active=True
            ).exists()
            and self.request.session.get("user_id") == self.request.user.id
        ):
            cart = Cart.objects.filter(
                session_id=self.request.session.session_key, active=True
            ).first()
            # assign cart to user
            cart.owner = self.request.user
            cart.save()
            # serializer = self.get_serializer(cart)

            self.request.session["cart_id"] = cart.cart_id
            self.request.session["user_id"] = self.request.user.id
            # assign cart to owner and return cart

            return cart

        # check if user has active cart. user might have a cart but have a new session created
        if Cart.objects.filter(owner=self.request.user, active=True).exists():
            cart = Cart.objects.filter(owner=self.request.user, active=True).first()

            return cart

        # check if user's session has an active cart, and session belongs to no one.assing cart session to request user
        if (
            Cart.objects.filter(
                session_id=self.request.session.session_key, active=True
            ).exists()
            and self.request.session.get("user_id") is None
        ):
            cart = Cart.objects.filter(
                session_id=self.request.session.session_key, active=True
            ).first()
            # assign cart to user
            cart.owner = self.request.user
            cart.save()

            self.request.session["cart_id"] = cart.cart_id
            self.request.session["user_id"] = self.request.user.id
            # assign cart to owner and return cart

            return cart

        # else just create a cart for user
        # create new session for new logged in user
        browser_accepts_cookies = self.does_browser_accepts_cookies()
        # associate user with cart
        cart = Cart.objects.create(
            owner=self.request.user, session_id=self.request.session.session_key
        )

        if browser_accepts_cookies:
            self.request.session["cart_id"] = cart.cart_id
            self.request.session["user_id"] = self.request.user.id

        return cart

    def perform_create_for_anonymous_user_with_session_id(self, serializer):
        """
        checks if anon user doesn't have an active cart in session
        creates cart for anon user.
        """

        # this user might have a cart

        # check if anon user has an active cart i.e user is still shooping
        if Cart.objects.filter(
            session_id=self.request.session.session_key, active=True
        ).exists():
            cart = Cart.objects.filter(
                session_id=self.request.session.session_key, active=True
            ).first()

            return cart

        # if a user doesn't have an active cart_id,
        # use session_id to create a new cart.
        cart = Cart.objects.create(session_id=self.request.session.session_key)
        # store cart_id in session_id - can override cart_id that is deactivated.
        self.request.session["cart_id"] = cart.cart_id
        # associate user with cart, another user might log in with same session
        return cart

    def perform_create_for_anonymous_user_without_session_id(self, serializer):
        """
        some browsers don't auto create sessions, check if that user has cookies enabled, 
        then create cart
        else, tell user to either  enable cookies or authenticate/login to create cart. 
        """

        browser_accepts_cookies = self.does_browser_accepts_cookies()
        # test that user accepts cookies
        if browser_accepts_cookies:
            # serializer.save(session_id=self.request.session.session_key)

            # create cart with session_id
            cart = Cart.objects.create(session_id=self.request.session.session_key)

            # store cart_id in session_id
            self.request.session["cart_id"] = cart.cart_id
            # self.request.session["user_id"] = self.request.user.id

            return None

        else:
            # need to throw an error message here
            # tell user to enable cookies or authenticate..
            # error hadled in view
            return None

