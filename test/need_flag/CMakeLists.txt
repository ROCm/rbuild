cmake_minimum_required (VERSION 2.8)
project(need_flag)

if(DEFINED SPECIAL_FLAG)
message(FATAL_ERROR "SPECIAL_FLAG defined")
endif()

find_package(ROCM NO_SYSTEM_ENVIRONMENT_PATH NO_CMAKE_ENVIRONMENT_PATH NO_CMAKE_SYSTEM_PATH)

include(ROCMInstallTargets)
include(ROCMSetupVersion)
include(ROCMCreatePackage)

rocm_setup_version(VERSION 1.0.0)

rocm_create_package(
    NAME need_flag 
    MAINTAINER "Amd amd@amd.com"
    LDCONFIG)

add_library(need_flag need_flag.cpp)

rocm_install_targets(TARGETS need_flag INCLUDE include)
