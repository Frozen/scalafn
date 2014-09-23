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

    from scalafn import List

    str1 = """blablabla@yandex.ru R=dnslookup T=remote_smtp H=mx.yandex.ru [127.0.0.1] X=TLS1.0:RSA_AES_256_CBC_SHA1:32"""
    str2 = """<> R=1XSUTD-0008L9-Vn U=Debian-exim P=local S=5035 T="Mail delivery failed: returning message to sender" for noreply@example.com"""
    import re

    rs1 = List(*re.split(" (?=\w=)", str1)).filter(lambda x: x.count("=")).toMap(lambda x: x.split("=", 1))

    assert rs1 == dict(
        R='dnslookup',
        T='remote_smtp',
        H='mx.yandex.ru [127.0.0.1]',
        X='TLS1.0:RSA_AES_256_CBC_SHA1:32'
    )

    rs2 = List(*re.split(" (?=\w=)", str2)).filter(lambda x: x.count("=")).toMap(lambda x: x.split("=", 1))
    assert rsw == dict(
        R='1XSUTD-0008L9-Vn',
        U='Debian-exim',
        P='local',
        S='5035',
        T='"Mail delivery failed: returning message to sender" for noreply@example.com'
    )
