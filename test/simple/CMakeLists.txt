cmake_minimum_required (VERSION 3.5)
project(simple)

find_package(ROCM NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_ENVIRONMENT_PATH NO_CMAKE_SYSTEM_PATH)

include(ROCMInstallTargets)
include(ROCMSetupVersion)
include(ROCMCreatePackage)

rocm_setup_version(VERSION 1.0.0)

rocm_create_package(
    NAME simple 
    MAINTAINER "Amd amd@amd.com"
    LDCONFIG)

add_library(simple simple.cpp)

rocm_install_targets(TARGETS simple INCLUDE include)
