from betterforms.multiform import MultiModelForm

from .CompanyCardForm import CompanyCardForm
from .CompanyInfoForm import CompanyInfoForm


class CompanyCardEditForm(MultiModelForm):
    form_classes = {
        'card': CompanyCardForm,
        'company': CompanyInfoForm
    }
