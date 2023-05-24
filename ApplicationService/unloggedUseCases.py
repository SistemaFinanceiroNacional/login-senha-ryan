from ApplicationService.OpenAccountUseCase import OpenAccountUseCase as oauc


class UnloggedUseCases:
    def __init__(self, open_use_case: oauc):
        self.open_use_case = open_use_case
