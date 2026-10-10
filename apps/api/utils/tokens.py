from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.models.user import User

class TokenGenerator(PasswordResetTokenGenerator):
    key_salt = "users.tokens.EmailVerificationTokenGenerator"

    def _make_hash_value(self, user: User, timestamp):
        return (
            f"{user.pk}:{timestamp}:{user.email}:"
            f"{user.email_verified_at}"
        )
