activate
========

Use ACTiVATED crack on Steam game

This script should be used only for fair purposes like making your own
backup copies of games you own on your account. It not supposed to be
used for piracy.

Install
-------

Install the ``activate`` package using your favourive method, e. g. `pipsi`_.

Copy latest ACTiVATED crack ``.so``-files to
``~/.local/share/activate/x86/libsteam_api.so`` and
``~/.local/share/activate/x86_64/libsteam_api.so``.

.. _pipsi: https://github.com/mitsuhiko/pipsi

Use
---

Go to game directory and enter ``activate``. The script may ask for
AppID if it can’t find it. That’s it.

::

    cd ~/Games/SuperSteamGame
    activate

It will replace libsteam_api.so files with ACTiVATED crack (of right
architecture), detect a version of Steam interfaces and fill
activated.ini files with right interfaces section.

To specify a custom username instead of “Cracked”, place it to
``~/.config/activate``::

    {
      "username": "ZeDoCaixao"
    }
