Welcome to iTensorPy's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   quickstart
   api
   examples
   contributing
   license

Introduction
===========

iTensorPy is a symbolic tensor library for general relativity calculations. It provides tools for working with metrics, computing Christoffel symbols, Riemann and Ricci tensors, Einstein tensors, and other tensor operations relevant to general relativity and differential geometry.

Features
--------

- Symbolic manipulation of tensor expressions using SymPy
- Metric tensor support with easy definition and manipulation
- Automatic computation of:
   - Christoffel symbols
   - Riemann curvature tensor
   - Ricci tensor and scalar
   - Einstein tensor
- Common spacetime metrics included:
   - Minkowski (flat spacetime)
   - Schwarzschild (spherically symmetric black hole)
   - Kerr (rotating black hole)
   - Friedmann-Lemaître-Robertson-Walker (cosmological)
   - de Sitter and Anti-de Sitter
- Support for custom metrics via dictionary input or file loading

Installation
===========

You can install iTensorPy using pip:

.. code-block:: bash

   pip install itensorpy

Or install from source:

.. code-block:: bash

   git clone https://github.com/yourusername/itensorpy.git
   cd itensorpy
   pip install -e .

Quick Example
===========

Here's a quick example to get you started:

.. code-block:: python

   import sympy as sp
   from sympy import symbols, sin
   from itensorpy import Metric, ChristoffelSymbols, RiemannTensor, RicciTensor

   # Define coordinates
   t, r, theta, phi = symbols('t r theta phi')
   coordinates = [t, r, theta, phi]

   # Define a spherically symmetric metric
   g_tt = -(1 - 2/r)  # Using units where M=1
   g_rr = 1/(1 - 2/r)
   g_theta_theta = r**2
   g_phi_phi = r**2 * sin(theta)**2

   # Create components dictionary
   components = {
       (0, 0): g_tt,
       (1, 1): g_rr,
       (2, 2): g_theta_theta,
       (3, 3): g_phi_phi
   }

   # Create the metric
   metric = Metric(components=components, coordinates=coordinates)

   # Compute Christoffel symbols
   christoffel = ChristoffelSymbols.from_metric(metric)
   print(christoffel)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 