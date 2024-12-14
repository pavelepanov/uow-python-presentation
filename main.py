from uowed import UnitOfWork
from gateway import UserGateway
from interactor import interactor


def main():
    uow = UnitOfWork()
    ugw = UserGateway(uow)
    interactor(uow, ugw)


if __name__ == '__main__':
    main()
