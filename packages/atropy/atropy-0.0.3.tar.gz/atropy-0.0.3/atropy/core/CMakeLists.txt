cmake_minimum_required(VERSION 3.27 FATAL_ERROR)
project(atropy_core
        VERSION 0.0.1
        DESCRIPTION "Dynamical low-rank solver for the kinetic CME"
        HOMEPAGE_URL https://git.uibk.ac.at/c7021158/kinetic-cme
        LANGUAGES CXX C)
enable_testing()

include(FetchContent)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake-modules")
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;Profile" CACHE STRING "" FORCE)


################################################################################
# General options
################################################################################

option("MKL_ENABLED" "Enable MKL for Ensign" OFF)
option("OPENMP" "Enable OpenMP" OFF)
option("PYBIND11_ENABLED" "Enable PYBIND" OFF)


################################################################################
# Compiler options
################################################################################

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(CMAKE_CXX_COMPILER_ID MATCHES Intel)
    set(CMAKE_CXX_FLAGS
      "${CMAKE_CXX_FLAGS} -Warn all"
    )
    set(CMAKE_CXX_FLAGS_DEBUG
      "-g -check all -traceback"
    )
    set(CMAKE_CXX_FLAGS_RELEASE
      "-O3 -ip -xHOST"
    )

else(CMAKE_CXX_COMPILER_ID MATCHES GNU)
    set(CMAKE_CXX_FLAGS
      "${CMAKE_CXX_FLAGS} -Wall"
    )
    set(CMAKE_CXX_FLAGS_DEBUG
      "-O0 -g3 -ggdb3 -Wall -D_GLIBCXX_DEBUG -fno-omit-frame-pointer -ftrapv"
    )
    set(CMAKE_CXX_FLAGS_RELEASE
      "-O3 -DNDEBUG -march=native -mtune=native"
    )
endif()


################################################################################
# External libraries
################################################################################

################################################################################
# cxxopts

FetchContent_Declare(cxxopts
  GIT_REPOSITORY "https://github.com/jarro2783/cxxopts.git"
  GIT_TAG "v3.2.1"
  GIT_SHALLOW ON
  GIT_PROGRESS ON
  FIND_PACKAGE_ARGS
)
FetchContent_MakeAvailable(cxxopts)


################################################################################
# Ensign

FetchContent_Declare(Ensign
  GIT_REPOSITORY https://github.com/leinkemmer/Ensign.git
  GIT_TAG "development"
  GIT_SHALLOW ON
  GIT_PROGRESS ON
  FIND_PACKAGE_ARGS
)
FetchContent_MakeAvailable(Ensign)


################################################################################
# pybind 11

if (PYBIND11_ENABLED)
  set(PYBIND11_NEWPYTHON ON)
  find_package(pybind11 REQUIRED)
endif()


################################################################################
# Create short-hands
################################################################################

# Create `input` and `output` directories
file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/input)
file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/output)

# Define short-hands for the src directory and the files
set(SRC ${CMAKE_CURRENT_SOURCE_DIR}/src)
set(SRC_FILES ${SRC}/bug_integrator.cpp
              ${SRC}/grid_class.cpp
              ${SRC}/matrix.cpp
              ${SRC}/print_functions.cpp
              ${SRC}/ps_integrator.cpp
              ${SRC}/tree_class.cpp)
set(HDR_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)


################################################################################
# Set up the program
################################################################################

if(PYBIND11_ENABLED)

  ################################################################################
  # pybind11

  pybind11_add_module(atropy_core_pybind11
    ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
    ${SRC_FILES}
  )

  # Add SOURCE_ROOT as a preprocessor directive
  target_compile_definitions(atropy_core_pybind11
    PRIVATE "SOURCE_ROOT=${CMAKE_CURRENT_SOURCE_DIR}"
  )

  target_compile_definitions(atropy_core_pybind11 PRIVATE "__PYBIND11__")

  target_include_directories(atropy_core_pybind11 PRIVATE ${HDR_DIR})
  target_link_libraries(atropy_core_pybind11 PRIVATE Ensign::Ensign)

  if(cxxopts_FOUND)
    target_link_libraries(atropy_core_pybind11 PRIVATE cxxopts::cxxopts)
  else()
    target_link_libraries(atropy_core_pybind11 PRIVATE cxxopts)
  endif()

  install(TARGETS atropy_core_pybind11 LIBRARY DESTINATION .)

else()

  ################################################################################
  # atropy_core

  add_executable(${PROJECT_NAME}
    ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
    ${SRC_FILES}
  )

  # Add SOURCE_ROOT as a preprocessor directive
  target_compile_definitions(${PROJECT_NAME}
    PRIVATE "SOURCE_ROOT=${CMAKE_CURRENT_SOURCE_DIR}"
  )

  target_include_directories(${PROJECT_NAME} PRIVATE ${HDR_DIR})
  target_link_libraries(${PROJECT_NAME} PRIVATE Ensign::Ensign)

  if(cxxopts_FOUND)
    target_link_libraries(${PROJECT_NAME} PRIVATE cxxopts::cxxopts)
  else()
    target_link_libraries(${PROJECT_NAME} PRIVATE cxxopts)
  endif()

  if(BUILD_TESTING)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests)
  endif()
endif()
