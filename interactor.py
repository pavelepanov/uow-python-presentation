from gateway import UserGateway
from entity import User
from uowed import UnitOfWork


def interactor(uow: UnitOfWork, ugw: UserGateway) -> None:
    user = ugw.get_user(1)
    user.name = 'Pavel'

    user2 = uow.register_new(User(id_=2, name='User2'))
    user2.name = 'Ilya'

    user3 = ugw.get_user(3)
    uow.register_deleted(user3)
    uow.commit()


def main():
    uow = UnitOfWork()
    ugw = UserGateway(uow)
    interactor(uow, ugw)


if __name__ == '__main__':
    main()

