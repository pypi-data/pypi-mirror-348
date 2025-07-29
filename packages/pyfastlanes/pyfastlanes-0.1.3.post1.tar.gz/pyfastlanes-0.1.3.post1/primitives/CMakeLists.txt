add_subdirectory(fls_generated)
add_subdirectory(fls)

add_library(primitives
        STATIC
        primitives.cpp
        ${FLS_GENERATED_OBJECT_FILES})


install(
        TARGETS primitives
        EXPORT FLSTargets        # Add to the export set
        LIBRARY DESTINATION lib          # For shared libraries
        ARCHIVE DESTINATION lib          # For static libraries
        RUNTIME DESTINATION bin          # For executables (if any)
)