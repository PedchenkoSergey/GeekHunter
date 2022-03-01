from .VacancyCreationForm import VacancyCreationForm


class VacancyEditForm(VacancyCreationForm):
    def save(self, commit=True):
        data = self.cleaned_data
        vacancy = super(VacancyEditForm, self).save()
        print(vacancy)
        for key in data:
            setattr(vacancy, key, data[key])
        vacancy.moderation_status = 'UNDER_REVIEW'
        vacancy.save()

        return vacancy
