#include "sax.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(sax_ts, m) {
  m.def("sax", &sax, "Apply SAX to a single time series.", py::arg("ts"),
        py::arg("window"), py::arg("stride") = 1, py::arg("w") = 15,
        py::arg("alpha") = 4);
  m.def("paa", &paa, "Apply PAA to a single time series.", py::arg("ts"),
        py::arg("window"), py::arg("stride") = 1, py::arg("w") = 15);
}