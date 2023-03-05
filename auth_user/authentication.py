from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
        self.model = self.get_model()
        try:
            token = self.model.objects.get(key=token)
        except self.model.DoesNotExist:
            return False, "Token does not exist"

        if not token.user.is_active:
            return False, "User inactive or deleted"

        # Below is implementation for token expiration
        # utc_now = datetime.utcnow()
        # utc_now = utc_now.replace(tzinfo=pytz.utc)
        #
        # if token.created < utc_now - timedelta(hours=24):
        #     raise (False, "Token has expired")

        return token.user, token


def check_auth(request):
    tokenAuth = CustomTokenAuthentication()
    try:
        auth_tok: str = request.headers.get("Authorization")
        assert(auth_tok.startswith("Bearer"))
        user, token_or_error = tokenAuth.authenticate_credentials(auth_tok.split()[-1])
    except KeyError as e:
        return False, None, {
            "logged_in": False,
            "errors": f'BadRequest: Missing Key, {e}',
        }
    if user:
        return True, user, {
            "logged_in": True,
        }
    else:
        return False, user, {
            "logged_in": False,
            "errors": token_or_error,
        }
