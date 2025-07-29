.. _prima.plugins.prima:
.. doctest docs/plugins/prima.rst

======================================
``prima`` : main plugin for Lino Prima
======================================

In Lino Prima this plugin defines the :xfile:`locale` directory for all
translations.

.. contents::
  :local:

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_prima.projects.prima1.settings')
>>> from lino.api.doctest import *
