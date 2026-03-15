#!/usr/bin/env python3
"""
Xengine CLI - Command Line Interface for Xengine Game Engine
Build, run, and deploy games across multiple platforms
"""

import os
import sys
import argparse
import subprocess
import json
import shutil
from pathlib import Path

class XengineCLI:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.build_dir = self.root_dir / "build"
        
    def create_project(self, name, language):
        """Create a new game project"""
        print(f"Creating new project: {name}")
        
        project_dir = Path(name)
        if project_dir.exists():
            print(f"Error: Directory {name} already exists")
            return False
        
        # Create project structure
        dirs = [
            project_dir / "assets" / "textures",
            project_dir / "assets" / "sounds",
            project_dir / "assets" / "music",
            project_dir / "assets" / "fonts",
            project_dir / "src",
            project_dir / "config"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create main game file based on language
        templates = {
            "nova": self._get_nova_template(),
            "vex": self._get_vex_template(),
            "cpp": self._get_cpp_template(),
            "dart": self._get_dart_template(),
            "corex": self._get_corex_template()
        }
        
        ext_map = {
            "nova": ".nova",
            "vex": ".vex",
            "cpp": ".cpp",
            "dart": ".dart",
            "corex": ".cx"
        }
        
        main_file = project_dir / "src" / f"main{ext_map.get(language, '.cpp')}"
        with open(main_file, 'w') as f:
            f.write(templates.get(language, templates["cpp"]))
        
        # Create config files
        self._create_config_files(project_dir, name)
        
        # Create README
        readme = f"""# {name}

A game built with Xengine Game Engine

## Building

```bash
xengine build
```

## Running

```bash
xengine run
```

## Deploying

### Android
```bash
xengine build --platform android
```

### iOS
```bash
xengine build --platform ios
```

### Web
```bash
xengine build --platform web
```
"""
        
        with open(project_dir / "README.md", 'w') as f:
            f.write(readme)
        
        print(f"Project {name} created successfully!")
        print(f"cd {name} && xengine run")
        return True
    
    def build(self, args):
        """Build the game"""
        platform = args.platform
        arch = args.arch
        config = args.config
        
        print(f"Building for {platform} ({arch}) in {config} mode...")
        
        # Create build directory
        build_path = self.build_dir / platform / arch / config
        build_path.mkdir(parents=True, exist_ok=True)
        
        # Run CMake
        cmake_cmd = [
            "cmake",
            "-S", ".",
            "-B", str(build_path),
            f"-DCMAKE_BUILD_TYPE={config.capitalize()}",
        ]
        
        # Platform-specific flags
        if platform == "android":
            cmake_cmd.extend([
                "-DXENGINE_BUILD_ANDROID=ON",
                f"-DANDROID_ABI={arch}",
                "-DANDROID_PLATFORM=android-21",
                f"-DCMAKE_TOOLCHAIN_FILE={os.environ.get('ANDROID_NDK')}/build/cmake/android.toolchain.cmake"
            ])
        elif platform == "ios":
            cmake_cmd.extend([
                "-DXENGINE_BUILD_IOS=ON",
                "-DCMAKE_SYSTEM_NAME=iOS",
                f"-DCMAKE_OSX_ARCHITECTURES={arch}"
            ])
        elif platform == "web":
            cmake_cmd.extend([
                "-DXENGINE_BUILD_WEB=ON",
                "-DCMAKE_TOOLCHAIN_FILE=$EMSDK/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake"
            ])
        
        try:
            subprocess.run(cmake_cmd, check=True)
            subprocess.run(["cmake", "--build", str(build_path)], check=True)
            
            print(f"Build complete! Output: {build_path}")
            
            # Run platform-specific packaging
            if platform == "android":
                self._package_apk(build_path, args)
            elif platform == "ios":
                self._package_ipa(build_path, args)
            elif platform == "web":
                self._package_web(build_path, args)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            return False
    
    def run(self, args):
        """Run the game"""
        platform = args.platform or self._detect_platform()
        
        print(f"Running game on {platform}...")
        
        if platform == "desktop":
            executable = self.build_dir / platform / "release" / "game"
            if sys.platform == "win32":
                executable = executable.with_suffix(".exe")
            
            if not executable.exists():
                print("Game not built. Building now...")
                args.platform = "desktop"
                args.arch = "x64"
                args.config = "release"
                self.build(args)
            
            subprocess.run([str(executable)])
        
        elif platform == "android":
            # Run on Android device/emulator
            apk = self.build_dir / "android" / "game.apk"
            if not apk.exists():
                print("APK not built. Building now...")
                args.platform = "android"
                args.arch = "arm64-v8a"
                args.config = "release"
                self.build(args)
            
            # Install and run
            subprocess.run(["adb", "install", "-r", str(apk)])
            subprocess.run(["adb", "shell", "am", "start", "-n", "com.xengine.game/.MainActivity"])
        
        elif platform == "web":
            # Serve web build
            web_dir = self.build_dir / "web"
            if not web_dir.exists():
                print("Web build not found. Building now...")
                args.platform = "web"
                args.arch = "wasm"
                args.config = "release"
                self.build(args)
            
            print(f"Serving game at http://localhost:8000")
            subprocess.run(["python3", "-m", "http.server", "--directory", str(web_dir)])
    
    def _package_apk(self, build_path, args):
        """Package game as Android APK"""
        print("Packaging APK...")
        
        apk_builder = self.root_dir / "tools" / "apk-builder.py"
        config_file = Path("config/android-config.json")
        
        cmd = [
            "python3",
            str(apk_builder),
            ".",
            "-o", str(self.build_dir / "android"),
            "-c", str(config_file)
        ]
        
        subprocess.run(cmd, check=True)
    
    def _package_ipa(self, build_path, args):
        """Package game as iOS IPA"""
        print("Packaging IPA...")
        
        # TODO: Implement IPA packaging
        pass
    
    def _package_web(self, build_path, args):
        """Package game for web"""
        print("Packaging for web...")
        
        web_dir = self.build_dir / "web"
        web_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        shutil.copy(build_path / "game.html", web_dir / "index.html")
        shutil.copy(build_path / "game.js", web_dir / "game.js")
        shutil.copy(build_path / "game.wasm", web_dir / "game.wasm")
        
        # Copy assets
        if Path("assets").exists():
            shutil.copytree("assets", web_dir / "assets", dirs_exist_ok=True)
    
    def _detect_platform(self):
        """Detect current platform"""
        if sys.platform == "win32":
            return "desktop"
        elif sys.platform == "darwin":
            return "desktop"
        elif sys.platform.startswith("linux"):
            return "desktop"
        return "desktop"
    
    def _get_nova_template(self):
        return '''program MyGame

import xengine.core
import xengine.graphics

fn main() {
    let engine = XEngine.create(EngineConfig {
        windowWidth: 1280,
        windowHeight: 720,
        windowTitle: "My Xengine Game"
    })
    
    while engine.isRunning() {
        engine.clearScreen(Color(0.2, 0.3, 0.8, 1.0))
        
        // Your game code here
        
        engine.present()
    }
    
    engine.shutdown()
}
'''
    
    def _get_vex_template(self):
        return '''import { useState, useEffect } from "@xengine/core"

component Game() {
    const [running, setRunning] = useState(true)
    
    render =>
        <GameCanvas width={1280} height={720}>
            <h1>My Xengine Game</h1>
            {/* Your game components here */}
        </GameCanvas>
}

export default Game
'''
    
    def _get_cpp_template(self):
        return '''#include <xengine/engine.h>

int main() {
    using namespace xengine;
    
    EngineConfig config;
    config.windowWidth = 1280;
    config.windowHeight = 720;
    config.appName = "My Xengine Game";
    
    Engine& engine = Engine::getInstance();
    engine.initialize(config);
    
    while (engine.isRunning()) {
        engine.update(engine.getDeltaTime());
        engine.render();
    }
    
    engine.shutdown();
    return 0;
}
'''
    
    def _get_dart_template(self):
        return '''import 'package:xengine/xengine.dart';

void main() {
  final engine = XEngine.create(
    EngineConfig(
      windowWidth: 1280,
      windowHeight: 720,
      appName: 'My Xengine Game',
    ),
  );
  
  while (engine.isRunning) {
    engine.update(engine.deltaTime);
    engine.render();
  }
  
  engine.shutdown();
}
'''
    
    def _get_corex_template(self):
        return'''#include <xengine/engine.h>

int main() {
    xengine::Engine engine;
    engine.init(1280, 720, "My Xengine Game");
    
    while (engine.isRunning()) {
        engine.update();
        engine.render();
    }
    
    engine.shutdown();
    return 0;
}
'''
    
    def _create_config_files(self, project_dir, name):
        """Create platform configuration files"""
        
        # Android config
        android_config = {
            "app_name": name,
            "package_name": f"com.xengine.{name.lower()}",
            "version_code": 1,
            "version_name": "1.0",
            "min_sdk": 21,
            "target_sdk": 33,
            "orientation": "landscape"
        }
        
        with open(project_dir / "config" / "android-config.json", 'w') as f:
            json.dump(android_config, f, indent=2)
        
        # iOS config
        ios_config = {
            "app_name": name,
            "bundle_id": f"com.xengine.{name.lower()}",
            "version": "1.0",
            "build": 1,
            "min_ios_version": "12.0"
        }
        
        with open(project_dir / "config" / "ios-config.json", 'w') as f:
            json.dump(ios_config, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Xengine Game Engine CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new game project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('-l', '--language', default='nova',
                              choices=['nova', 'vex', 'cpp', 'dart', 'corex'],
                              help='Programming language')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build the game')
    build_parser.add_argument('--platform', default='desktop',
                             choices=['desktop', 'android', 'ios', 'web'],
                             help='Target platform')
    build_parser.add_argument('--arch', default='x64',
                             choices=['x64', 'x86', 'arm64-v8a', 'armeabi-v7a', 'wasm'],
                             help='Target architecture')
    build_parser.add_argument('--config', default='release',
                             choices=['debug', 'release'],
                             help='Build configuration')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run the game')
    run_parser.add_argument('--platform', default=None,
                           choices=['desktop', 'android', 'web'],
                           help='Platform to run on')
    
    args = parser.parse_args()
    
    cli = XengineCLI()
    
    if args.command == 'create':
        cli.create_project(args.name, args.language)
    elif args.command == 'build':
        cli.build(args)
    elif args.command == 'run':
        cli.run(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
