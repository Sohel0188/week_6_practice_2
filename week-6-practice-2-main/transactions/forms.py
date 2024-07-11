from django import forms
from .models import Transaction
from core.models import BankInfo
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        bankinfo = BankInfo.objects.first()
        if bankinfo.is_bankrupt == True :
            raise forms.ValidationError(
                f'Sorry, Bank is Bankrupted'
            )

            # return amount
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount
    
class TransferAmountFormssss(TransactionForm):
    account_number = forms.CharField(max_length=20)  # Add account_number field

    class Meta(TransactionForm.Meta):
        fields = TransactionForm.Meta.fields + ['account_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # Add any specific validation logic for amount if needed
        return amount

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        # Add any specific validation logic for account_number if needed
        # For example, check if the account number exists or is valid
        if not self.is_valid_account_number(account_number):
            raise forms.ValidationError("Invalid account number.")
        return account_number
    
    
    
class TransferAmountForm(forms.Form):
    
    account_no = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight border-gray-500 focus:outline-none focus:shadow-outline'
        })
    )
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight border-gray-500 focus:outline-none focus:shadow-outline'
        })
    )
   