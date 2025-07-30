// =============================================================================
//  Project       : GenomeNinja
//  File          : src/genome_ninja/_cpp/src/seq_gc.cpp
//
//  Author        : Qinzhong Tian <tianqinzhong@qq.com>
//  Created       : 2025/4/29 16:32
//  Last Updated  : 2025/4/29 16:32            // auto-update on save
//
//  Description   : Calculate GC content of DNA sequences using SeqAn3
//                 Supports common sequence file formats like FASTA/FASTQ
//                 Provides Python binding interface for testing and validation
//
//  C++ Standard  : C++23
//  Version       : 0.1.0                       // auto-bump on save
//
//  Usage         : g++ seq_gc.cpp -std=c++23 -I<seqan3_include_path> -I<pybind11_include_path>
//
//  Copyright © 2025 Qinzhong Tian. All rights reserved.
//  License       : MIT – see LICENSE in project root for full text.
// =============================================================================
#include <seqan3/io/sequence_file/input.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

// ---------- Core Algorithm ----------
double gc_percent(const std::string& path)
{
    using seqan3::operator""_dna5;
    seqan3::sequence_file_input fin{path};
    uint64_t gc = 0, total = 0;
    for (auto & [seq, id, qual] : fin)
        for (auto base : seq)
            total++, gc += (base == 'G'_dna5 || base == 'C'_dna5);
    return total ? 100.0 * gc / total : 0.0;
}

// ---------- Register Functions ----------
void register_seq_gc(py::module_ &m)
{
    m.def("gc_percent", &gc_percent,
          py::arg("fasta"),
          "Compute GC% using SeqAn3 FASTA reader");
}
