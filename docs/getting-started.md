# Getting Started with Xengine

## Introduction

Xengine is a powerful multi-language game engine that lets you create 2D and 3D games for mobile, desktop, and web platforms. This guide will help you create your first game.

## Installation

### Prerequisites

Before installing Xengine, ensure you have:

- **C++ Compiler**: GCC 9+, Clang 10+, or MSVC 2019+
- **CMake**: Version 3.15 or higher
- **Python**: Version 3.7 or higher
- **Git**: For cloning the repository

### Platform-Specific Requirements

**Windows:**
- Visual Studio 2019 or later
- Windows SDK 10.0.19041.0 or later

**macOS:**
- Xcode 12 or later
- macOS 10.15 or later

**Linux:**
```bash
sudo apt-get install build-essential cmake ninja-build \
    libgl1-mesa-dev libx11-dev libxrandr-dev libxinerama-dev \
    libxcursor-dev libxi-dev libasound2-dev
```

### Building Xengine

1. Clone the repository:
```bash
git clone https://github.com/yourusername/xengine.git
cd xengine
```

2. Initialize submodules:
```bash
git submodule update --init --recursive
```

3. Build the engine:
```bash
mkdir build && cd build
cmake .. -G Ninja
ninja
```

4. Install (optional):
```bash
sudo ninja install
```

## Your First Game

### Creating a Project

Create a new directory for your game:

```bash
mkdir my-game
cd my-game
```

Create a `game.nova` file:

```nova
program MyFirstGame

import xengine.core
import xengine.graphics

fn main() {
    println("Creating my first game!")
    
    // Initialize engine
    let engine = XEngine.create(EngineConfig {
        windowWidth: 800,
        windowHeight: 600,
        windowTitle: "My First Game"
    })
    
    // Create a sprite
    let player = engine.createSprite("player.png")
    player.setPosition(Vec2(400, 300))
    player.setSize(64, 64)
    
    // Game loop
    while engine.isRunning() {
        // Clear screen
        engine.clearScreen(Color(0.2, 0.3, 0.8, 1.0))
        
        // Draw sprite
        player.draw()
        
        // Present frame
        engine.present()
    }
    
    engine.shutdown()
}
```

### Running Your Game

```bash
xengine run game.nova
```

## Core Concepts

### 1. Engine Initialization

Every Xengine game starts by creating an engine instance:

```nova
let engine = XEngine.create(EngineConfig {
    windowWidth: 1280,
    windowHeight: 720,
    windowTitle: "My Game",
    fullscreen: false,
    vsync: true,
    targetFPS: 60
})
```

### 2. Game Loop

The game loop is the heart of your game:

```nova
while engine.isRunning() {
    // 1. Process input
    Input.update()
    
    // 2. Update game logic
    update(engine.getDeltaTime())
    
    // 3. Render
    render()
    
    // 4. Present to screen
    engine.present()
}
```

### 3. Sprites

Sprites are 2D images:

```nova
let sprite = engine.createSprite("character.png")
sprite.setPosition(Vec2(100, 100))
sprite.setSize(64, 64)
sprite.setRotation(45.0)  // degrees
sprite.setColor(Color(1, 1, 1, 0.5))  // Semi-transparent
sprite.draw()
```

### 4. Input Handling

```nova
// Keyboard
if Input.isKeyPressed(KEY_SPACE) {
    println("Space pressed!")
}

if Input.isKeyJustPressed(KEY_ENTER) {
    println("Enter just pressed!")
}

// Mouse
let mousePos = Input.getMousePosition()
if Input.isMouseButtonPressed(MOUSE_LEFT) {
    println("Mouse at: ", mousePos)
}

// Touch (mobile)
if Input.getTouchCount() > 0 {
    let touch = Input.getTouch(0)
    println("Touch at: ", touch.position)
}

// Gamepad
if Input.isGamepadButtonPressed(0, GAMEPAD_A) {
    println("Controller A button!")
}
```

### 5. Physics

Add physics to your game:

```nova
// Create physics world
let physics = engine.createPhysicsWorld2D()
physics.setGravity(Vec2(0, -9.8))

// Create dynamic body
let body = physics.createRigidBody(RigidBodyType.Dynamic)
body.setPosition(Vec2(400, 300))
body.addBoxCollider(64, 64)
body.setMass(1.0)

// Apply forces
body.applyForce(Vec2(100, 0))
body.applyImpulse(Vec2(0, 500))

// Update physics
physics.update(deltaTime)
```

### 6. Audio

Play sounds and music:

```nova
// Load and play sound effect
Audio.loadSound("jump.wav")
Audio.playSound("jump.wav")

// Load and play music
Audio.loadMusic("background.ogg")
Audio.playMusic("background.ogg", true)  // Loop

// 3D positional audio
let source = Audio.createSource3D()
source.setPosition(Vec3(10, 0, 5))
source.setSound("ambient.wav")
source.play()
```

### 7. Scenes

Organize your game with scenes:

```nova
struct GameScene {
    player: Player
    enemies: [Enemy]
    score: int
}

fn createGameScene() -> GameScene {
    return GameScene {
        player: createPlayer(),
        enemies: [
            createEnemy(100, 100),
            createEnemy(200, 100),
            createEnemy(300, 100)
        ],
        score: 0
    }
}

fn updateGameScene(scene: &GameScene, deltaTime: float) {
    updatePlayer(&scene.player, deltaTime)
    
    for enemy in &scene.enemies {
        updateEnemy(enemy, deltaTime)
    }
    
    checkCollisions(scene)
}

fn renderGameScene(scene: GameScene) {
    renderPlayer(scene.player)
    
    for enemy in scene.enemies {
        renderEnemy(enemy)
    }
    
    drawText("Score: " + scene.score.toString(), Vec2(20, 700))
}
```

## Building for Different Platforms

### Desktop (Windows/Mac/Linux)

```bash
# Build for current platform
xengine build --platform desktop

# Output: build/desktop/game
```

### Android (APK)

```bash
# Build APK
xengine build --platform android --arch arm64-v8a

# Output: build/android/game.apk

# Install on device
adb install build/android/game.apk
```

### iOS (IPA)

```bash
# Build IPA
xengine build --platform ios --arch arm64

# Output: build/ios/game.ipa
```

### Web (HTML5/WebAssembly)

```bash
# Build for web
xengine build --platform web

# Output: build/web/index.html

# Serve locally
python3 -m http.server --directory build/web
```

## Project Structure

Recommended project structure:

```
my-game/
├── assets/          # Game assets
│   ├── textures/    # Images and sprites
│   ├── sounds/      # Audio files
│   ├── music/       # Background music
│   └── fonts/       # Font files
├── src/             # Source code
│   ├── main.nova    # Entry point
│   ├── player.nova  # Player code
│   └── enemy.nova   # Enemy code
├── build/           # Build output
├── config/          # Build configurations
│   ├── android-config.json
│   ├── ios-config.json
│   └── web-config.json
└── README.md
```

## Next Steps

- Read the [API Reference](api-reference.md)
- Explore [Sample Games](../examples/)
- Learn about [Graphics Programming](graphics.md)
- Understand [Physics Systems](physics.md)
- Setup [Mobile Development](mobile-build.md)

## Getting Help

- [Documentation](https://docs.xengine.dev)
- [Forum](https://forum.xengine.dev)
- [Discord](https://discord.gg/xengine)
- [GitHub Issues](https://github.com/yourusername/xengine/issues)

## Common Issues

### Build Errors

**CMake not found:**
```bash
# Ubuntu/Debian
sudo apt-get install cmake

# macOS
brew install cmake

# Windows
# Download from cmake.org
```

**Missing dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-dev libx11-dev

# macOS
# Install Xcode command line tools
xcode-select --install
```

### Runtime Errors

**"Failed to create window":**
- Check if your graphics drivers are up to date
- Try running with `--render-api opengl` flag

**"Asset not found":**
- Verify asset paths are correct
- Ensure assets are in the `assets/` directory
- Check file permissions

### Performance Issues

**Low FPS:**
- Enable VSync: `vsync: true` in config
- Reduce render resolution
- Use sprite batching
- Profile with `--enable-profiler` flag

**High memory usage:**
- Unload unused assets
- Use texture atlases
- Compress audio files
- Enable asset streaming

---

Happy game development with Xengine! 🎮
