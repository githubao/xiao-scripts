#!/usr/bin/env python
# encoding: utf-8

"""
@description: new meta call init

@author: baoqiang
@time: 2018/9/27 上午11:01
"""


class AA(object):
    def __new__(cls, *args, **kwargs):  # 静态方法，self需要自己传递
        print('new in AA', args, kwargs)
        return super(AA, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):  # 普通方法，self会自动绑定
        print('init in AA', args, kwargs)
        super(AA, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):  # 普通方法，self会自动绑定
        print('call in AA', args, kwargs)
        # return super(AA, self).__call__(*args,**kwargs)


class BB(type):
    def __new__(mcs, name, bases, attrs):  # 静态方法，self需要自己传递
        print('new in BB', name, bases, attrs)
        return super(BB, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, *args, **kwargs):  # 普通方法，self会自动绑定
        print('init in BB', args, kwargs)
        super(BB, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):  # 普通方法，self会自动绑定
        print('call in BB', args, kwargs)
        return super(BB, cls).__call__(*args, **kwargs)


class CC(AA, metaclass=BB):
    '一旦执行定义类CC的代码，就会调用BB元类中的__new__方法，其中真正生成类CC的是super(BB, self)中的__new__，也就是type中的__new__方法,检查返回对象是否是BB的实例，若是则调用type(CC).__init__(CC)，也就是BB元类中的__init__方法，来初始化CC对象'

    # __metaclass__ = BB

    def __new__(cls, *args, **kwargs):  # 静态方法，self需要自己传递
        print('new in CC', args, kwargs)
        return super(CC, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):  # 普通方法，self会自动绑定
        print('init in CC', args, kwargs)
        super(CC, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):  # 普通方法，self会自动绑定
        print('call in CC', args, kwargs)
        return super(CC, self).__call__(*args, **kwargs)


def run():
    """
    new in BB CC (<class '__main__.AA'>,) {'__module__': '__main__', '__qualname__': 'CC', '__doc__': '一旦执行定义类CC的代码，就会调用BB元类中的__new__方法，其中真正生成类CC的是super(BB, self)中的__new__，也就是type中的__new__方法,检查返回对象是否是BB的实例，若是则调用type(CC).__init__(CC)，也就是BB元类中的__init__方法，来初始化CC对象', '__new__': <function CC.__new__ at 0x109769510>, '__init__': <function CC.__init__ at 0x109769598>, '__call__': <function CC.__call__ at 0x109769620>, '__classcell__': <cell at 0x109734468: empty>}
    init in BB ('CC', (<class '__main__.AA'>,), {'__module__': '__main__', '__qualname__': 'CC', '__doc__': '一旦执行定义类CC的代码，就会调用BB元类中的__new__方法，其中真正生成类CC的是super(BB, self)中的__new__，也就是type中的__new__方法,检查返回对象是否是BB的实例，若是则调用type(CC).__init__(CC)，也就是BB元类中的__init__方法，来初始化CC对象', '__new__': <function CC.__new__ at 0x109769510>, '__init__': <function CC.__init__ at 0x109769598>, '__call__': <function CC.__call__ at 0x109769620>, '__classcell__': <cell at 0x109734468: BB object at 0x7fc4f76c2e18>}) {}
    call in BB () {}
    new in CC () {}
    new in AA () {}
    init in CC () {}
    init in AA () {}
    call in CC () {}
    call in AA () {}
    :return:
    """

    c = CC()
    c()


if __name__ == '__main__':
    run()
