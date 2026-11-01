cmake_minimum_required (VERSION 3.5)
project(need_env)

if(NOT "$ENV{SPECIAL_ENV}" STREQUAL "1")
message(FATAL_ERROR "SPECIAL_ENV not set")
endif()

find_package(ROCM NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_ENVIRONMENT_PATH NO_CMAKE_SYSTEM_PATH)

include(ROCMInstallTargets)
include(ROCMSetupVersion)
include(ROCMCreatePackage)

rocm_setup_version(VERSION 1.0.0)

rocm_create_package(
    NAME need_env 
    MAINTAINER "Amd amd@amd.com"
    LDCONFIG)

add_library(need_env need_env.cpp)

rocm_install_targets(TARGETS need_env INCLUDE include)
