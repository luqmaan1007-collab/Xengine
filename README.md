# Xengine - Multi-Language Game Engine

**Xengine** is a powerful, modular 2D and 3D game engine for creating high-performance games that run on mobile (Android/iOS), desktop (Windows/Mac/Linux), and web platforms.

## 🎮 Supported Programming Languages

Xengine supports development in multiple languages:

- **Nova** - Memory-safe compiled language
- **Vex** - React-like UI framework with custom syntax
- **Swift** - Modern Apple ecosystem language
- **C++** - High-performance native development
- **C** - Low-level systems programming
- **Dart** - Flutter-compatible development
- **Corex** - C++ like language for AAA games
- **Nexar** - Dart-like language with Flutter-style UI

## 🚀 Key Features

### Cross-Platform Export
- **APK** - Android application packages
- **IPA** - iOS application bundles
- **Native Binaries** - Windows (.exe), macOS (.app), Linux (ELF)
- **Web** - HTML5/WebGL/WebAssembly
- **Console** - PlayStation, Xbox, Nintendo Switch (with appropriate SDKs)

### Graphics & Rendering

**Low-Level Graphics API**
- OpenGL ES 3.0 / OpenGL 4.5 / Vulkan / Metal support
- Shader-based immediate mode rendering
- Multiple render techniques (single-pass, multi-pass)
- Dynamic vertex/index buffer creation
- Texture support: 1D, 2D, 3D, Cubemaps
- Texture formats: DDS, JPG, PNG, TGA, KTX, ASTC
- Occlusion queries
- Fullscreen mode
- Screenshot capture
- Video playback (WebM, MP4, H.264, H.265)

**High-Level Rendering**
- **Forward Renderer** - Unlimited lights, shadow mapping
- **Deferred Renderer** - Advanced lighting and post-effects
- **PBR Renderer** - Physical

ly-based rendering
- **2D Renderer** - Optimized sprite batching
- Post-processing effects: Bloom, DOF, Motion Blur, SSAO, SSR
- Particle systems
- GPU skinning (4-weight)
- Morph target animation

### Physics

**3D Physics**
- Rigid body dynamics
- Collision shapes: Sphere, Box, Capsule, Cylinder, Cone, Convex Hull, Triangle Mesh
- Constraints: Point-to-Point, Hinge, Cone Twist, 6DOF, Slider
- Ray casting and sweep tests
- Character controller
- Cloth simulation
- Soft body physics

**2D Physics**
- Box2D-based physics simulation
- Shapes: Circle, Box, Polygon
- Joints: Distance, Revolute, Prismatic, Pulley, Gear
- Collision detection and response

### Audio

- 3D positional audio
- Audio formats: OGG, WAV, MP3, FLAC
- Audio effects: Reverb, Echo, Low-pass filter
- Audio streaming for large files
- Multi-channel audio mixing
- HRTF support for spatial audio

### Animation

- Skeletal animation with GPU skinning
- Blend trees for smooth transitions
- Animation layers and masking
- Inverse kinematics (IK)
- Procedural animation
- Timeline-based cutscene system

### Scene Management

- Hierarchical scene graph
- Spatial partitioning: Octree, KD-Tree, BSP
- Frustum culling
- LOD (Level of Detail) system
- Asset streaming
- Scene serialization (JSON, Binary)

### Networking

- WebSockets support
- HTTP/HTTPS requests
- Real-time multiplayer
- NAT traversal
- Peer-to-peer connections
- Server authoritative architecture

### Input

- Keyboard, Mouse, Touch, Gamepad support
- Custom input mapping
- Gesture recognition
- Virtual joystick for mobile

### UI System

- Immediate mode UI (ImGui-style)
- Retained mode UI with layout engine
- Rich text rendering
- UI animations
- Accessibility support

### Asset Pipeline

- Asset compression and optimization
- Texture atlas generation
- Model optimization and LOD generation
- Audio conversion and compression
- Shader compilation and optimization
- Asset bundling and encryption

## 📦 Installation

### Quick Start (3 commands)

```bash
cd xengine
chmod +x build.sh install.sh
./build.sh
```

That's it! The demo will run automatically.

### Manual Build

```bash
cd xengine
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
./xengine_demo
```

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake g++
```

**macOS:**
```bash
brew install cmake
xcode-select --install
```

**Windows:**
- Install Visual Studio 2019+ with C++ tools
- Install CMake from https://cmake.org

## 🎯 Quick Start

### Example Game in Nova

```nova
program SpaceShooter

import xengine.graphics
import xengine.input
import xengine.audio

fn main() {
    let engine = XEngine.create()
    let window = engine.createWindow(800, 600, "Space Shooter")
    
    let player = engine.createSprite("player.png")
    player.position = Vec2(400, 300)
    
    while engine.isRunning() {
        engine.update()
        
        if Input.isKeyPressed(KEY_LEFT) {
            player.position.x -= 5
        }
        if Input.isKeyPressed(KEY_RIGHT) {
            player.position.x += 5
        }
        
        engine.render()
    }
}
```

### Example Game in Vex

```vex
import { XEngine, Sprite, Input } from "@xengine/core"

component Game() {
    const [playerX, setPlayerX] = useState(400)
    
    useEffect(() => {
        const engine = XEngine.create()
        
        engine.onUpdate(() => {
            if (Input.isKeyPressed("ArrowLeft")) {
                setPlayerX(x => x - 5)
            }
            if (Input.isKeyPressed("ArrowRight")) {
                setPlayerX(x => x + 5)
            }
        })
    }, [])
    
    render =>
        <GameCanvas width={800} height={600}>
            <Sprite src="player.png" x={playerX} y={300} />
        </GameCanvas>
}
```

### Example Game in C++

```cpp
#include <xengine/engine.h>
#include <xengine/graphics.h>
#include <xengine/input.h>

int main() {
    using namespace xengine;
    
    Engine engine;
    Window* window = engine.createWindow(800, 600, "Space Shooter");
    
    Sprite player("player.png");
    player.position = Vec2(400, 300);
    
    while (engine.isRunning()) {
        engine.update();
        
        if (Input::isKeyPressed(KEY_LEFT)) {
            player.position.x -= 5.0f;
        }
        if (Input::isKeyPressed(KEY_RIGHT)) {
            player.position.x += 5.0f;
        }
        
        engine.render();
    }
    
    return 0;
}
```

### Example Game in Dart/Nexar

```dart
import 'package:xengine/xengine.dart';

void main() {
  final engine = XEngine.create();
  final window = engine.createWindow(800, 600, 'Space Shooter');
  
  final player = Sprite('player.png')
    ..position = Vector2(400, 300);
  
  while (engine.isRunning) {
    engine.update();
    
    if (Input.isKeyPressed(Key.arrowLeft)) {
      player.position.x -= 5;
    }
    if (Input.isKeyPressed(Key.arrowRight)) {
      player.position.x += 5;
    }
    
    engine.render();
  }
}
```

## 🛠️ Building for Different Platforms

### Android (APK)

```bash
xengine build --platform android --arch arm64-v8a
# Output: build/android/game.apk
```

### iOS (IPA)

```bash
xengine build --platform ios --arch arm64
# Output: build/ios/game.ipa
```

### Windows

```bash
xengine build --platform windows --arch x64
# Output: build/windows/game.exe
```

### Web (HTML5/WebAssembly)

```bash
xengine build --platform web
# Output: build/web/index.html
```

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Graphics Programming](docs/graphics.md)
- [Physics Guide](docs/physics.md)
- [Audio System](docs/audio.md)
- [Networking](docs/networking.md)
- [Building for Mobile](docs/mobile-build.md)
- [Performance Optimization](docs/optimization.md)

## 🎨 Sample Games

- **2D Platformer** - Classic side-scrolling platformer
- **3D FPS** - First-person shooter with multiplayer
- **Racing Game** - 3D racing game with physics
- **RPG** - Turn-based RPG with inventory system
- **Puzzle Game** - Match-3 puzzle game
- **Tower Defense** - Real-time strategy tower defense

## 🏗️ Project Structure

```
xengine/
├── src/              # Engine source code
│   ├── core/        # Core engine systems
│   ├── graphics/    # Rendering systems
│   ├── physics/     # Physics engine
│   ├── audio/       # Audio system
│   ├── network/     # Networking
│   └── platform/    # Platform-specific code
├── bindings/         # Language bindings
│   ├── nova/
│   ├── vex/
│   ├── swift/
│   ├── cpp/
│   ├── c/
│   ├── dart/
│   ├── corex/
│   └── nexar/
├── tools/            # Build tools and utilities
│   ├── asset-pipeline/
│   ├── shader-compiler/
│   └── apk-builder/
├── examples/         # Example games
├── docs/             # Documentation
└── tests/            # Unit and integration tests
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

Xengine is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🌟 Features Comparison with Other Engines

| Feature | Xengine | Unity | Unreal | Godot |
|---------|---------|-------|--------|-------|
| Multiple Languages | ✅ 8 languages | ❌ C# only | ❌ C++ only | ❌ GDScript/C# |
| APK Export | ✅ | ✅ | ✅ | ✅ |
| Native Binaries | ✅ | ✅ | ✅ | ✅ |
| Web Export | ✅ | ✅ | ⚠️ Limited | ✅ |
| Open Source | ✅ | ❌ | ⚠️ Source access | ✅ |
| 2D Physics | ✅ | ✅ | ✅ | ✅ |
| 3D Physics | ✅ | ✅ | ✅ | ✅ |
| PBR Rendering | ✅ | ✅ | ✅ | ✅ |
| Custom Shaders | ✅ | ✅ | ✅ | ✅ |

## 💬 Community & Support

- [Discord Server](https://discord.gg/xengine)
- [Forum](https://forum.xengine.dev)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/xengine)
- [GitHub Discussions](https://github.com/yourusername/xengine/discussions)

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Core engine architecture
- ✅ Multi-language support
- ✅ Cross-platform rendering
- ✅ Physics systems (2D & 3D)
- ✅ Audio system
- ✅ APK/IPA export

### Version 1.5
- 🔄 Visual scripting system
- 🔄 Advanced particle systems
- 🔄 Ray tracing support
- 🔄 VR/AR support
- 🔄 Console export (PS5, Xbox Series, Switch)

### Version 2.0
- 📋 Cloud multiplayer services
- 📋 Built-in marketplace
- 📋 AI-assisted development tools
- 📋 Live collaboration features
- 📋 Mobile AR framework

---

**Made with ❤️ by the Xengine Team**
