from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  


# Custom token generator class for account activation, inheriting from PasswordResetTokenGenerator.
# This class generates a token based on user information and timestamp.
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
        )
# Create an instance of the custom token generator for account activation.
account_activation_token = AccountActivationTokenGenerator()