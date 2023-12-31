.. |pyproj| raw:: html

    <a href="https://pyproj4.github.io/pyproj/stable/" target="_blank">``pyproj``</a>

.. |requests| raw:: html

    <a href="https://docs.python-requests.org/en/stable/" target="_blank">``requests``</a>

.. |github| raw:: html

    <a href="https://github.com/iannesbitt/pyegt" target="_blank">github</a>

Installation
#####################################

``pyegt`` can be installed from pip, conda, or from source.
The only dependencies are |pyproj| (``pyproj>=3.1.0``) and |requests|.

pip
-------------------------------------

To install with pip, create your virtual environment, then run::

    pip install pyegt

conda
-------------------------------------

You can use anaconda (or miniconda) to install either the package itself,
or a virtual environment set up specifically for ``pyegt``.

The following will install pyegt from the ``iannesbitt`` channel::

    conda install -c iannesbitt pyegt

To create a new environment for ``pyegt`` and then install::

    conda create -n pyegt -c iannesbitt pyegt

From source
-------------------------------------

``pyegt`` source code is on |github|. To install the latest commit manually,
execute the following::

    git clone https://github.com/iannesbitt/pyegt
    cd pyegt
    pip install .

Or, to install the latest commit directly from github using pip::

    pip install git+https://github.com/iannesbitt/pyegt
