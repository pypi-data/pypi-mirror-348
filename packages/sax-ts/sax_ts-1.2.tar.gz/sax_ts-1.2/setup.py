from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "1.2"

ext_modules = [
    Pybind11Extension(
        "sax_ts",
        ["src/bind.cpp", "src/sax.cpp"],
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="sax_ts",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
