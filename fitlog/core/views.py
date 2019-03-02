from django.urls import reverse
from django.views.generic import RedirectView


class HomePageRedirectView(RedirectView):
    """
    Homepage view which redirect user on:
    - login page for anonymous
    - training list page ?
    """
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        if user.is_anonymous:
            return reverse('login')

        # @todo
        return reverse('login')
        #
        # bankaccounts = BankAccount.objects.get_user_bankaccounts(user)
        # if len(bankaccounts) == 1:
        #
        #     return reverse('banktransactions:list', kwargs={
        #         'bankaccount_pk': bankaccounts.first().pk,
        #     })
        #
        # return reverse('bankaccounts:list')
