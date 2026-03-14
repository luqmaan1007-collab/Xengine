cmake_minimum_required(VERSION 3.15)
project(Xengine VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build options
option(XENGINE_BUILD_SAMPLES "Build sample games" ON)
option(XENGINE_BUILD_TESTS "Build unit tests" ON)
option(XENGINE_BUILD_TOOLS "Build asset pipeline tools" ON)
option(XENGINE_ENABLE_VULKAN "Enable Vulkan renderer" OFF)
option(XENGINE_ENABLE_METAL "Enable Metal renderer (macOS/iOS)" OFF)
option(XENGINE_BUILD_ANDROID "Build for Android (APK)" OFF)
option(XENGINE_BUILD_IOS "Build for iOS (IPA)" OFF)
option(XENGINE_BUILD_WEB "Build for Web (WASM)" OFF)

# Platform detection
if(WIN32)
    set(XENGINE_PLATFORM "Windows")
    add_definitions(-DXENGINE_PLATFORM_WINDOWS)
elseif(APPLE)
    if(IOS)
        set(XENGINE_PLATFORM "iOS")
        add_definitions(-DXENGINE_PLATFORM_IOS)
    else()
        set(XENGINE_PLATFORM "macOS")
        add_definitions(-DXENGINE_PLATFORM_MACOS)
    endif()
elseif(ANDROID)
    set(XENGINE_PLATFORM "Android")
    add_definitions(-DXENGINE_PLATFORM_ANDROID)
elseif(EMSCRIPTEN)
    set(XENGINE_PLATFORM "Web")
    add_definitions(-DXENGINE_PLATFORM_WEB)
else()
    set(XENGINE_PLATFORM "Linux")
    add_definitions(-DXENGINE_PLATFORM_LINUX)
endif()

message(STATUS "Building Xengine for ${XENGINE_PLATFORM}")

# Source files
set(XENGINE_CORE_SOURCES
    src/core/engine.cpp
)

# Collect all sources
set(XENGINE_SOURCES
    ${XENGINE_CORE_SOURCES}
)

# Create engine library
add_library(xengine STATIC ${XENGINE_SOURCES})

# Include directories
target_include_directories(xengine PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Platform-specific dependencies
if(WIN32)
    target_link_libraries(xengine PUBLIC
        winmm
        ws2_32
    )
elseif(APPLE)
    find_library(COCOA_LIBRARY Cocoa)
    find_library(IOKIT_LIBRARY IOKit)
    find_library(COREVIDEO_LIBRARY CoreVideo)
    target_link_libraries(xengine PUBLIC
        ${COCOA_LIBRARY}
        ${IOKIT_LIBRARY}
        ${COREVIDEO_LIBRARY}
    )
elseif(UNIX AND NOT APPLE)
    target_link_libraries(xengine PUBLIC
        ${CMAKE_DL_LIBS}
        pthread
    )
endif()

# Simple example executable
add_executable(xengine_demo examples/simple/main.cpp)
target_link_libraries(xengine_demo PRIVATE xengine)

# Install
install(TARGETS xengine xengine_demo
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(DIRECTORY src/
    DESTINATION include/xengine
    FILES_MATCHING PATTERN "*.h"
)
