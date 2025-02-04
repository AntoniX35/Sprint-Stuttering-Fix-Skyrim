cmake_minimum_required(VERSION 3.30)
message("Using toolchain file ${CMAKE_TOOLCHAIN_FILE}.")

# -------------------------------------------------- Setup project ----------------------------------------------------
project(
  SprintStutteringFix
  VERSION 1.0.0
  LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_OPTIMIZE_DEPENDENCIES ON)

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/version.rc.in
  ${CMAKE_CURRENT_BINARY_DIR}/version.rc
  @ONLY
)
macro(set_from_environment VARIABLE)
	if (NOT DEFINED ${VARIABLE} AND DEFINED ENV{${VARIABLE}})
		set(${VARIABLE} $ENV{${VARIABLE}})
	endif ()
endmacro()
set_from_environment(SkyrimPath)
# -------------------------------------------------- Add sources ------------------------------------------------------
file(
  GLOB_RECURSE
  sources
  CONFIGURE_DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
  ${CMAKE_CURRENT_BINARY_DIR}/version.rc
)
list(REMOVE_ITEM sources ${CMAKE_CURRENT_SOURCE_DIR}/include/PCH.h)

source_group(
  TREE ${CMAKE_CURRENT_SOURCE_DIR}
  FILES ${sources}
)

# -------------------------------------------------- Add dependencies -------------------------------------------------
find_package(CommonLibSSE CONFIG REQUIRED)

find_path(SIMPLEINI_INCLUDE_DIRS SimpleIni.h)

# -------------------------------------------------- Setup DLL --------------------------------------------------------
add_commonlibsse_plugin(
  ${PROJECT_NAME}
  AUTHOR Antonix35
  SOURCES ${sources}
)

add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

target_include_directories(
  ${PROJECT_NAME}
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${SIMPLEINI_INCLUDE_DIRS}
)

target_precompile_headers(
  ${PROJECT_NAME}
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include/PCH.h
  ${SIMPLEINI_INCLUDE_DIRS}/SimpleIni.h
)

target_compile_options(
  ${PROJECT_NAME}
  PRIVATE
  /cgthreads8 /diagnostics:caret /jumptablerdata /MP /W4 /Zc:__cplusplus /Zc:enumTypes /Zc:inline /Zc:templateScope
)

if(CMAKE_BUILD_TYPE STREQUAL RelWithDebInfo)
  target_compile_options(
    ${PROJECT_NAME}
    PRIVATE
    /fp:fast /Ob3 /GL /GR- /Gw /Qpar
  )
  target_link_options(
    ${PROJECT_NAME}
    PRIVATE
    /CGTHREADS:8 /INCREMENTAL:NO /OPT:REF,ICF=4
  )
endif()

# -------------------------------------------------- Post-build -------------------------------------------------------
if(CMAKE_BUILD_TYPE STREQUAL Debug)
  set(BUILD_NAME Debug)
else()
  set(BUILD_NAME Release)
endif()

add_custom_command(
  TARGET ${PROJECT_NAME}
  POST_BUILD
  COMMAND 
  ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${PROJECT_NAME}> ${SkyrimPath}/SKSE/Plugins/
  COMMAND
  ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Config/${PROJECT_NAME}.ini ${SkyrimPath}/SKSE/Plugins/
  COMMAND
  ${CMAKE_COMMAND} -E copy $<TARGET_PDB_FILE:${PROJECT_NAME}> ${SkyrimPath}/SKSE/Plugins/
  COMMAND
  ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/SKSE/Plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/SKSE/Plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy $<TARGET_PDB_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/SKSE/Plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Config/${PROJECT_NAME}.ini ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/SKSE/Plugins
)

file(GLOB_RECURSE OUTPUT_DLLS ${CMAKE_CURRENT_SOURCE_DIR}/contrib/*.dll)

set_property(
  TARGET ${PROJECT_NAME}
  APPEND PROPERTY ADDITIONAL_CLEAN_FILES ${OUTPUT_DLLS} ${OUTPUT_PDBS}
)

# ---- Build artifacts ----

set(SCRIPT "scripts/archive_artifacts.py")
set(TARGET_NAME "archive")

add_custom_target(
	create_artifact
	COMMAND
		"${CMAKE_CURRENT_SOURCE_DIR}/${SCRIPT}"
		"--name=\"${PROJECT_NAME}\""
		"--dll=\"$<TARGET_FILE:${PROJECT_NAME}>\""
		"--pdb=\"$<TARGET_PDB_FILE:${PROJECT_NAME}>\""
        "--ini=${CMAKE_CURRENT_SOURCE_DIR}/contrib/Config/${PROJECT_NAME}.ini"
        
	WORKING_DIRECTORY
		${CMAKE_CURRENT_BINARY_DIR}
	SOURCES
		${SCRIPT}
)

add_dependencies(
	create_artifact
	${PROJECT_NAME}
)

source_group(
	TREE ${CMAKE_CURRENT_SOURCE_DIR}
	FILES ${SCRIPT}
)
