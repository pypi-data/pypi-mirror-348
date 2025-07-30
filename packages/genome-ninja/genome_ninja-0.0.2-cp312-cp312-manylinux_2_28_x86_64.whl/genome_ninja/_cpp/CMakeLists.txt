cmake_minimum_required(VERSION 3.18)
project(genome_ninja_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_EXTENSIONS OFF)

if(CMAKE_VERSION VERSION_LESS 3.30 AND CMAKE_CXX_COMPILER_ID STREQUAL "IntelLLVM")
  message(WARNING "IntelLLVM requires CMake 3.30 or later for C++23")
endif()

set(PYBIND11_FINDPYTHON ON)

# ---------- Dependencies ----------
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP COMPONENTS CXX QUIET)
find_package(ZLIB QUIET)

if(NOT ZLIB_FOUND)
  message(STATUS "System ZLIB not found. Fetching ZLIB using FetchContent.")
  include(FetchContent)
  FetchContent_Declare(
    zlib
    GIT_REPOSITORY https://github.com/madler/zlib.git
    GIT_TAG v1.3.1
    URL https://www.zlib.net/zlib-1.3.1.tar.gz
    URL_HASH SHA256=9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  )
  FetchContent_MakeAvailable(zlib)

  if(TARGET zlibstatic AND NOT TARGET ZLIB::ZLIB)
    add_library(ZLIB::ZLIB ALIAS zlibstatic)
    message(STATUS "Aliased zlibstatic to ZLIB::ZLIB.")
  elseif(TARGET zlib AND NOT TARGET ZLIB::ZLIB)
    add_library(ZLIB::ZLIB ALIAS zlib)
    message(STATUS "Aliased zlib to ZLIB::ZLIB.")
  endif()

  set(ZLIB_FOUND TRUE CACHE BOOL "ZLIB was fetched and made available" FORCE)
else()
  message(STATUS "Found system ZLIB. Using ZLIB::ZLIB target: ${ZLIB_LIBRARIES}")
endif()

if(NOT TARGET ZLIB::ZLIB)
  message(FATAL_ERROR "ZLIB target ZLIB::ZLIB is not available after attempting to find or fetch. This is required for SeqAn3 and other dependencies.")
endif()

# ---------- SIMDe ----------
set(SIMDE_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libs/simde")
include_directories(${SIMDE_INCLUDE_DIR})

# ---------- SeqAn3 ----------
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/libs/seqan3/cmake")

set(SEQAN3_ABS_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libs/seqan3/include")
set(SEQAN3_ABS_CLONE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libs/seqan3")

set(SEQAN3_INCLUDE_DIR "${SEQAN3_ABS_INCLUDE_DIR}"
    CACHE PATH "Absolute path to SeqAn3 include directory provided by parent project")
set(SEQAN3_CLONE_DIR "${SEQAN3_ABS_CLONE_DIR}"
    CACHE PATH "Absolute path to SeqAn3 clone directory provided by parent project")

add_subdirectory(libs/seqan3 EXCLUDE_FROM_ALL)

# ---------- helper macro ----------
function(add_gninja_module modname bind_cpp impl_glob)
  pybind11_add_module(${modname} ${bind_cpp})
  file(GLOB SRC_FILES CONFIGURE_DEPENDS ${impl_glob})
  target_sources(${modname} PRIVATE ${SRC_FILES})
  target_link_libraries(${modname} PRIVATE
        ZLIB::ZLIB seqan3::seqan3
        $<$<BOOL:${OpenMP_CXX_FOUND}>:OpenMP::OpenMP_CXX>)
  target_compile_definitions(${modname} PRIVATE
        $<$<CONFIG:Release>:SIMDE_ENABLE_NATIVE_ALIASES>)
  install(TARGETS ${modname} LIBRARY DESTINATION genome_ninja)
endfunction()

# ----------- add modules -----------
add_gninja_module(_gninja_test  bindings/test_bind.cpp  test/*.cpp)
