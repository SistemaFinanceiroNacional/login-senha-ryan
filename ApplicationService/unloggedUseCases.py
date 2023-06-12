from ApplicationService.registerclientusecase import (
    RegisterClientUseCase as RegisterCase
)


class UnloggedUseCases:
    def __init__(self, register_client: RegisterCase):
        self.register_client = register_client
