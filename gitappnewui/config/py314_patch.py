"""
Патч для Python 3.14 + Django < 5.2.
Без него Django Admin падает: AttributeError: 'super' object has no attribute 'dicts'
Исправлено в Django 5.2+, этот файл — запасной вариант для 5.1.
"""
import sys
from copy import copy as copy_obj


def apply():
    if sys.version_info < (3, 14):
        return

    from django.template import context as ctx

    def _base_context_copy(self):
        duplicate = ctx.BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__ = copy_obj(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    ctx.BaseContext.__copy__ = _base_context_copy
