#!/usr/bin/env python3
"""
Xengine APK Builder
Builds Android APK packages from Xengine games
"""

import os
import sys
import subprocess
import shutil
import argparse
import json
from pathlib import Path

class APKBuilder:
    def __init__(self, project_path, output_path):
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.build_dir = self.project_path / "build" / "android"
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = {
            "android": "Android SDK",
            "ndk-build": "Android NDK",
            "gradle": "Gradle build system",
            "adb": "Android Debug Bridge"
        }
        
        for tool, name in required_tools.items():
            if not shutil.which(tool):
                print(f"Error: {name} ({tool}) not found in PATH")
                return False
        
        return True
    
    def create_android_project(self, config):
        """Create Android project structure"""
        print("Creating Android project structure...")
        
        # Create directories
        dirs = [
            self.build_dir / "app" / "src" / "main" / "java",
            self.build_dir / "app" / "src" / "main" / "res" / "layout",
            self.build_dir / "app" / "src" / "main" / "res" / "values",
            self.build_dir / "app" / "src" / "main" / "res" / "drawable",
            self.build_dir / "app" / "src" / "main" / "assets",
            self.build_dir / "app" / "src" / "main" / "jniLibs" / "arm64-v8a",
            self.build_dir / "app" / "src" / "main" / "jniLibs" / "armeabi-v7a",
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create AndroidManifest.xml
        manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{config['package_name']}">
    
    <uses-feature android:glEsVersion="0x00030000" android:required="true" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.VIBRATE" />
    
    <application
        android:label="{config['app_name']}"
        android:icon="@drawable/ic_launcher"
        android:allowBackup="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
        
        <activity
            android:name=".MainActivity"
            android:screenOrientation="{config.get('orientation', 'landscape')}"
            android:configChanges="orientation|keyboardHidden|screenSize"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        
        with open(self.build_dir / "app" / "src" / "main" / "AndroidManifest.xml", "w") as f:
            f.write(manifest)
        
        # Create build.gradle
        gradle = f'''apply plugin: 'com.android.application'

android {{
    compileSdkVersion {config.get('compile_sdk', 33)}
    buildToolsVersion "{config.get('build_tools', '33.0.0')}"
    ndkVersion "{config.get('ndk_version', '25.1.8937393')}"
    
    defaultConfig {{
        applicationId "{config['package_name']}"
        minSdkVersion {config.get('min_sdk', 21)}
        targetSdkVersion {config.get('target_sdk', 33)}
        versionCode {config.get('version_code', 1)}
        versionName "{config.get('version_name', '1.0')}"
        
        ndk {{
            abiFilters 'arm64-v8a', 'armeabi-v7a'
        }}
    }}
    
    buildTypes {{
        release {{
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt')
        }}
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
}}'''
        
        with open(self.build_dir / "app" / "build.gradle", "w") as f:
            f.write(gradle)
        
        # Create MainActivity.java
        package_path = config['package_name'].replace('.', '/')
        java_dir = self.build_dir / "app" / "src" / "main" / "java" / package_path
        java_dir.mkdir(parents=True, exist_ok=True)
        
        main_activity = f'''package {config['package_name']};

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;

public class MainActivity extends Activity {{
    static {{
        System.loadLibrary("xengine");
        System.loadLibrary("game");
    }}
    
    private native void nativeInit();
    private native void nativeUpdate();
    private native void nativeShutdown();
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        // Fullscreen
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        // Keep screen on
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        
        // Hide system UI
        View decorView = getWindow().getDecorView();
        decorView.setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );
        
        nativeInit();
    }}
    
    @Override
    protected void onDestroy() {{
        nativeShutdown();
        super.onDestroy();
    }}
}}'''
        
        with open(java_dir / "MainActivity.java", "w") as f:
            f.write(main_activity)
    
    def compile_native_code(self, config):
        """Compile native C/C++ code for Android"""
        print("Compiling native code...")
        
        # Build for arm64-v8a
        cmd = [
            "cmake",
            "-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake",
            "-DANDROID_ABI=arm64-v8a",
            "-DANDROID_PLATFORM=android-21",
            "-DXENGINE_BUILD_ANDROID=ON",
            "-S", str(self.project_path),
            "-B", str(self.build_dir / "native" / "arm64-v8a")
        ]
        
        subprocess.run(cmd, check=True)
        subprocess.run(["cmake", "--build", str(self.build_dir / "native" / "arm64-v8a")], check=True)
        
        # Copy libraries
        shutil.copy(
            self.build_dir / "native" / "arm64-v8a" / "libgame.so",
            self.build_dir / "app" / "src" / "main" / "jniLibs" / "arm64-v8a" / "libgame.so"
        )
    
    def copy_assets(self):
        """Copy game assets to Android assets folder"""
        print("Copying assets...")
        
        assets_src = self.project_path / "assets"
        assets_dst = self.build_dir / "app" / "src" / "main" / "assets"
        
        if assets_src.exists():
            shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
    
    def build_apk(self, config):
        """Build the APK using Gradle"""
        print("Building APK...")
        
        os.chdir(self.build_dir)
        
        # Build release APK
        cmd = ["./gradlew", "assembleRelease"]
        subprocess.run(cmd, check=True)
        
        # Copy APK to output
        apk_src = self.build_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        apk_dst = self.output_path / f"{config['app_name']}.apk"
        
        shutil.copy(apk_src, apk_dst)
        print(f"APK created: {apk_dst}")
    
    def sign_apk(self, config):
        """Sign the APK with keystore"""
        if 'keystore' in config:
            print("Signing APK...")
            
            cmd = [
                "jarsigner",
                "-verbose",
                "-sigalg", "SHA256withRSA",
                "-digestalg", "SHA-256",
                "-keystore", config['keystore'],
                "-storepass", config['storepass'],
                str(self.output_path / f"{config['app_name']}.apk"),
                config['key_alias']
            ]
            
            subprocess.run(cmd, check=True)
            print("APK signed successfully")
    
    def build(self, config_file):
        """Main build process"""
        # Load config
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Build steps
        try:
            self.create_android_project(config)
            self.compile_native_code(config)
            self.copy_assets()
            self.build_apk(config)
            
            if config.get('sign_apk', False):
                self.sign_apk(config)
            
            print("Build completed successfully!")
            return True
            
        except Exception as e:
            print(f"Build failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Build Xengine game to Android APK')
    parser.add_argument('project', help='Path to game project')
    parser.add_argument('-o', '--output', default='build', help='Output directory')
    parser.add_argument('-c', '--config', default='android-config.json', help='Build configuration file')
    
    args = parser.parse_args()
    
    builder = APKBuilder(args.project, args.output)
    
    config_path = Path(args.project) / args.config
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        print("Creating default config...")
        
        default_config = {
            "app_name": "XengineGame",
            "package_name": "com.xengine.game",
            "version_code": 1,
            "version_name": "1.0",
            "min_sdk": 21,
            "target_sdk": 33,
            "compile_sdk": 33,
            "orientation": "landscape"
        }
        
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    success = builder.build(config_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
