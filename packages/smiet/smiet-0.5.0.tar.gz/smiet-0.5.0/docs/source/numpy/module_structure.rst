Module structure
================

The module contains two classes related to the template synthesis algorithm:
``TemplateSynthesis`` and ``SliceSynthesis``. The latter is not meant to be used directly, but is used
internally by the former. The ``TemplateSynthesis`` class is the main class of the module and it the
one which should be used to perform the synthesis.

It also has several classes which make it easy to load in CoREAS simulations stored as `HDF5` files.
These are the ``SlicedShower`` and the ``SlicedShowerCherenkov`` classes. They are both subclasses of
the ``Shower`` and ``CoREASHDF5`` classes, which each implement one of the two core aspects of air shower
simulations.

Reading in CoREAS simulations
-----------------------------

A sliced CoREAS simulation is one which is set up such that each antenna has its radio signal split
into the contributions coming from different atmospheric slices. The width of these slices should be
a constant (in atmospheric depth) and the number of slices should be the same for each antenna. In
CoREAS v1.4 this behaviour is achieved by adding multiple copies of the same physical antenna on the
ground, but configure each to only accept emission from a certain atmospheric depth range. This is done
using the `slantdepth` keyword. For more information, please refer to the
`CoREAS documentation <https://web.iap.kit.edu/huege/downloads/coreas-manual.pdf>`_.

The ``SlicedShower`` class is meant to be used with simulations where each slice is configured with
the same antennas on the ground. This is the standard for template synthesis. When reading in the
CoREAS `HDF5` file, the magnetic field, core, geometry and longitudinal profile are retrieved and stored
as attributes. The antenna names are retrieved and stored in the ``ant_names`` attribute. Here it is
important to note that the antenna names are assumed to be in the format ``{name}x{atmospheric_depth}``.
To find all the unique antenna names, the antenna names are split on the ``x`` character and the first
element is stored in a set, which is eventually stored as the ``ant_names`` attribute.

.. important::
    The antenna names are assumed to be in the format ``{antenna_name}x{atmospheric_depth}``. This is
    naming scheme is used by the :doc:`CORSIKA tools<../corsika/corsika_index>` in this package.

Apart from the name, the antenna position is also retrieved and stored in the ``ant_dict`` attribute.
This is done by looping over all unique antenna names and reading the position of the antenna configured
for atmospheric depth 5 g/cm2 (i.e. ``x5`` is appended to the antenna name to find the entry in the `HDF5`
file).

.. important::
    Inside of the ``CoREASHDF5`` class and its children, the positions are still stored in the
    CORSIKA coordinate system. The units are however already converted to internal units.

.. todo::
    Remove the hardcoded slice value of 5 for the antenna positions.

The number of slices present in a ``SlicedShower`` is then calculated as the number of observers in
the `HDF5` file divided by the number of unique antenna names. This is stored in the ``nr_slices``
attribute. Finally, the atmospheric model number is read from the simulations settings. If this
number is present in the ``models.atm_models`` dictionary from `radiotools <https://c-glaser.de/physics/radiotools/>`_,
the ``Atmosphere`` object is created and stored as the ``atmosphere`` attribute.

It is also possible to set up simulations where each slice has antennas placed at the same
viewing angle in units of local Cherenkov angle. As the Cherenkov angle is dependent on the atmospheric
depth, this implies a different set of antennas for each slice. It can be useful to opt for this
approach when checking the validity of the template synthesis algorithm or to recalculate the spectral
parameters. For these simulations the ``SlicedShowerCherenkov`` class can be used. It essentially lifts
some of the assumptions made in ``SlicedShower`` about the naming of the antennas. This does result in
slightly more memory consumption and a longer loading time.

An atmospheric slice
--------------------

In the NumPy version of the template synthesis package, a single slice of the atmosphere is represented
by a class called ``SliceSynthesis``. Its responsibility is to keep track of all the slice specific
variables, such as the atmospheric depth of the slice, the viewing angles of antennas with respect to
this slice and the amplitude/phase spectra of the radio signal in this slice.

.. warning::
    While it can be very useful to interact with the ``SliceSynthesis`` class directly for debugging,
    we advise against relying on it for scripting purposes. It does not exist in the JAX implementation,
    which makes scripts who rely on this class not easily portable. Instead, we recommend using the
    convenience functions provided by the ``TemplateSynthesis`` class to retrieve slice specific
    variables.

The ``SliceSynthesis`` class stores all its variables in a structured NumPy array, which can be accessed
through its ``antenna_parameters`` property. Two of the fields in this array are `distance` and `viewing_angle`.
These hold the distance from the slice to each antenna and the viewing angle of each antenna, respectively.
Note that these values are updated during the template generation **and** the mapping process, so be sure
to check which steps have been run before interpreting these values.

The other fields of the array contain the amplitude and phase spectra for the geomagnetic and charge-
excess components of the radio signal. These are normalised with respect to the shower geometry. For
the amplitude this means scaling with distance as well as some other factors. There is also the
normalisation using the spectral parameters, interpolated to the viewing angle of the antenna.

.. math::

    A_{\text{geo}} &= \\
    A_{\text{ce}} &= \\

The phases are adapted by adding a linear phase gradient corresponding to the arrival time of the
signal as calculated using the shower geometry. The arrival time is calculated using the distance :math:`D`
from the slice to the ground along the shower axis and the distance :math:`L` from the slice to antenna,
corrected by the effective refractive index :math:`n_{eff}`.

.. math::

    t_{obs} &= \frac{ L \times n_{eff} - D }{ c } \\
    \phi &= \phi + 2 \pi f t_{obs}

Here :math:`c` is the speed of light in vacuum. During the template generation this correction
essentially moves the peak of the pulse to the very first time bin. Then, when mapping to a target,
the peak is moved back to expected time bin based on its geometry.

Synthesising an entire shower
-----------------------------

The ``TemplateSynthesis`` class stores all the slices of the origin shower, each represented by a
``SliceSynthesis`` object, in a list. Furthermore, it acts a central location for all the information
that is shared between the slices, such as the atmospheric model, the shower geometry, the antenna
positions, the valid frequencies and the spectral parameters which are currently loaded.
When creating a template (or loading one from disk) all these attributes are linked to the slices
in the list.

.. attention::
    As Python does not really have the concept of pointers, the attributes of the ``TemplateSynthesis``
    object do **not** serve as the source of truth for the shared variables. This is to say, if you
    update for example the atmosphere of the ``TemplateSynthesis`` object, the slices will not
    automatically receive this update. They will still hold references to the original atmosphere.

