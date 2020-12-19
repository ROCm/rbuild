cmake_minimum_required (VERSION 2.8)
project(simple)

find_package(ROCM)

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
