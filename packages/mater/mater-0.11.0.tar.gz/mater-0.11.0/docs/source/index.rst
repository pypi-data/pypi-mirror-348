.. MATER documentation master file, created by
   sphinx-quickstart on Thu Apr 25 09:13:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. To hide the the title header of a page, add to the top of the page:
.. :sd_hide_title: 

:html_theme.sidebar_secondary.remove: true

.. warning::
   It is a demonstration version for review only. It means that the model is not complete, the data are fake and the taxonomy may change in a close future. 
   We are currently working on the dataset through many collaborations with academic partners and private institutes such as 
   `Carbone 4 <https://www.ifinitiative.com/01---en---home-copy>`_ or `Schneider Electric <https://www.se.com/ww/en>`_.

=============================
MATER |release| documentation
=============================

**MATER** (*Metabolic Analysis for Transdisciplinary Ecological Research*) is a flexible open source software originally developped in Grenoble (France) at `ISTerre <https://www.isterre.fr>`_. 
It is a biophysical foundation for modeling constrained transition scenarios.

.. grid:: 1 2 2 2
    :gutter: 4
    :padding: 2 2 0 0
    :class-container: sd-text-center

    .. grid-item-card:: Overview
        :shadow: md

        Want to find out more about the team's scientific approach?
        The *Overview* section summarizes the concept of the model and places it in the academic literature.

        +++

        .. button-ref:: overview
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Toward science

    .. grid-item-card::  User Guide
        :shadow: md

        The *user guide* provides infromations on installing the model environment, running your first simulation
        and visualizing the outputs.

        +++

        .. button-ref:: user_guide
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            To the user guide

    .. grid-item-card::  Technical Reference
        :shadow: md

        The reference guide contains a detailed description of the MATER model equations and the MATER modules API.

        +++

        .. button-ref:: technical_reference
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            To the reference guide

    .. grid-item-card::  Contributing
        :shadow: md

        Want to help us in our project ? See the contribution guidelines and welcome aboard !

        +++

        .. button-ref:: contributing
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            To the contribution guide

.. toctree::
   :maxdepth: 4
   :hidden:

   overview/index
   user_guide/index
   technical_reference/index
   contributing/index

   

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


