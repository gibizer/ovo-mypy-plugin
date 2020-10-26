.. image:: https://travis-ci.org/gibizer/ovo-mypy-plugin.svg?branch=main
    :target: https://travis-ci.org/gibizer/ovo-mypy-plugin

===============
ovo-mypy-plugin
===============
This module provides a mypy plugin for oslo.versionedobjects library as well
as incomplete type stubs defining types for o.vo fields.

Usage
-----

Add the following to your mypy config to enable the plugin

.. code:: ini

    [mypy]
    plugins = ovo_mypy_plugin.plugin

The plugin will define every o.vo field with type ``Any`` and enforce that only
the defined fields can be used in your code.

If you add the ``ovo_stubs`` to your mypy path then the o.vo fields will have
the type define based on the fields stubs instead of ``Any``.

.. code:: ini

    [mypy]
    mypy_path = ./ovo_stub/

By default the plugin processes o.vos that are **directly** inheriting from
``oslo_versionedobjects.base.VersionedObject`` class or decorated with a
decorators defined in ``oslo_versionedobjects.base.VersionedObjectRegistry``.

If your project uses its own direct base class then you can specify the name of
the class in the ``OVO_MYPY_BASE_CLASSES`` environment variable. You can
specify more than one class names separated by space.

If your project uses its own registry class then you can specify the name of
the class in the ``OVO_MYPY_DECORATOR_CLASSES`` environment variable. You can
specify more than one class names separated by space.

