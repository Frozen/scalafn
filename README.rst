****************************************
Scalafn: scala-like lists usage
****************************************


============
Installation
============

pip install git+git://github.com/Frozen/scalafn.git@master


=====
Usage
=====


Hello World:


.. code-block:: python
    # You can't use this code in ipython, because symbol _ means "last command". Use import _ as X
    >>> from scalafn import List, _
    >>> a = List(1, 2, 3)
    >>> a.map(lambda x : x*2)
    [2, 4, 6]

    >>> a.map(_ * 2)
    [2, 4, 6]

    >>> a.map(_ / 2.0)
    [0.5, 1, 1.5]

    >>> a.map(6.0 / _)
    [6.0, 3.0, 2.0]

    >>> a.map(_ + 1).map(_ * 5).filter(_ < 20)
    [10, 15]

    >>> a.filter(_ > 2)
    [3]

    >>> a.filterNot(_ > 2)
    [1, 2]

    >>> List(0, 1, True, False, '').filter(_)
    [1, True]

    >>> class My():
    >>>     def __init__(self, v):
    >>>         self.v = v
    >>>
    >>>     def get_v(self):
    >>>         return self.v

    >>> b = List(My(0), My(1), My(2), My(3))

    >>> b.map(_.v)
    [0, 1, 2, 3]

    >>> b.map(_.get_v())
    [0, 1, 2, 3]

    >>> b.filter(_.v)
    [My(1), My(2), My(3)]

    >>> b.filter(_.get_v() > 2)
    [My(3)]
