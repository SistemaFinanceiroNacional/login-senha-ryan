from ApplicationService.registerclientusecase import (
    RegisterClientUseCase as rcuc
)


class UnloggedUseCases:
    def __init__(self, register_client: rcuc):
        self.register_client = register_client
