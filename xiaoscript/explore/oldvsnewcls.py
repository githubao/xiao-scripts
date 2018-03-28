#!/usr/bin/env python
# encoding: utf-8

"""
@description: 新式类和旧式类的区别

@author: pacman
@time: 2018/3/28 10:22
"""


class A:
    def save(self):
        print('this is A')


class B(A):
    pass


class C(A):
    def save(self):
        print('this is C')


class D(B, C):
    """
    mro:
    (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
    """


class E:
    __slots__ = ('id', 'name')


class F:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        return 'default'

    def __getattribute__(self, item):
        print('__getattribute__ is invoked')


def run():
    a = D()
    a.save()


def run2():
    print(D.__mro__)


def run3():
    a = D()

    print(a.__class__)
    print(type(a))

    print(D.__bases__)


def run4():
    """
    type 是 所有实例的根, class也是一种实例，他们是通过 type new出来的

    object 是 所有类型的根，type也是一种类型，它的父类是object，通过它可以new 出来class实例

    :return:
    """

    # 这个表示的是 object这个实例，是通过谁产生的，cls的实例都是通过type类产生的
    # 下面这两条语句是等价的
    # <class 'type'>
    print(object.__class__)
    print(type(object))

    # 这个表示type这个类的父类是谁，type的父类是object的啊
    # <class 'object'>
    print(type.__bases__[0])


def run5():
    e = E()
    e.name = 3
    # e.name2 = 3


def run6():
    """
    __getattr__ 方法在属性不存在的时候被调用
    __getattribute__ 如果在子类中override，那么所有的属性获取都会调用该方法。
    而且如果定义的该方法，那么除非在__getattribute__显示调用__getattr__或者在__getattribute__抛出异常，否则不会调用__getattr__

    :return:
    """

    f = F("xiao")
    f.id = 3


def main():
    # run()
    # run2()
    # run3()
    # run4()
    # run5()
    run6()


if __name__ == '__main__':
    main()
