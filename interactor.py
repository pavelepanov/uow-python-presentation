from gateway import UserGateway
from entity import User
from uowed import UnitOfWork


def interactor(uow: UnitOfWork, ugw: UserGateway) -> None:
    user = ugw.get_user(1)
    user.name = 'Pavel'

    user2 = uow.register_new(User(2, 'User2'))
    user2.name = 'Ilya'

    user3 = ugw.get_user(3)
    uow.register_deleted(user3)
    uow.commit()
