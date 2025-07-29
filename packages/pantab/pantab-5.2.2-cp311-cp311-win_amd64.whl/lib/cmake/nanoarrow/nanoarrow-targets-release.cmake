#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nanoarrow::nanoarrow_static" for configuration "Release"
set_property(TARGET nanoarrow::nanoarrow_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nanoarrow::nanoarrow_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/nanoarrow_static.lib"
  )

list(APPEND _cmake_import_check_targets nanoarrow::nanoarrow_static )
list(APPEND _cmake_import_check_files_for_nanoarrow::nanoarrow_static "${_IMPORT_PREFIX}/lib/nanoarrow_static.lib" )

# Import target "nanoarrow::nanoarrow_shared" for configuration "Release"
set_property(TARGET nanoarrow::nanoarrow_shared APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nanoarrow::nanoarrow_shared PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/nanoarrow_shared.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/nanoarrow_shared.dll"
  )

list(APPEND _cmake_import_check_targets nanoarrow::nanoarrow_shared )
list(APPEND _cmake_import_check_files_for_nanoarrow::nanoarrow_shared "${_IMPORT_PREFIX}/lib/nanoarrow_shared.lib" "${_IMPORT_PREFIX}/bin/nanoarrow_shared.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
