__all__ = []


from toolbox51.common.singleton import SingletonMeta


__all__ += ["NotGiven", "NOT_GIVEN"]
class NotGiven(metaclass=SingletonMeta):
    def __bool__(self):
        return False
NOT_GIVEN = NotGiven()

__all__ += ["PlaceHolder"]
class PlaceHolder:
    def __new__(cls, *args, **kwargs):
        raise TypeError("占位符，不可实例化")