// =============================================================================
//  Project       : GenomeNinja
//  File          : src/genome_ninja/_cpp/bindings/test_bind.cpp
//
//  Author        : Qinzhong Tian <tianqinzhong@qq.com>
//  Created       : 2025/4/29 16:50
//  Last Updated  : 2025-04-29 18:00
//
//  Description   : Implementation file for Python binding test module
//                  For testing and validating Python interfaces of GenomeNinja core functionalities
//
//  C++ Standard  : C++23
//  Version       : 0.1.4
//
//  Usage         : cmake .. -DCMAKE_BUILD_TYPE=Release    // Recommended to build with CMake
//                  make                                    // Compile to generate Python module
//
//  Copyright © 2025 Qinzhong Tian. All rights reserved.
//  License       : MIT – see LICENSE in project root for full text.
// =============================================================================
#include <pybind11/pybind11.h>
namespace py = pybind11;

void register_seq_gc(py::module_&);

PYBIND11_MODULE(_gninja_test, m) {
    m.doc() = "Test submodule";
    register_seq_gc(m);
}
