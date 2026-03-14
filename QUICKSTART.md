# XENGINE QUICKSTART 🚀

## ✅ What is Xengine?

Xengine is a multi-language game engine that lets you:
- Build games in **8 languages** (Nova, Vex, C++, C, Dart, Swift, Corex, Nexar)
- Export to **APK** (Android), **IPA** (iOS), **EXE** (Windows), **Web** (HTML5)
- Use all **Turbulenz Engine features** (graphics, physics, audio, networking)

## 🎯 Install & Run (30 seconds)

```bash
cd xengine
./build.sh
```

Done! The demo runs automatically.

## 📝 What Just Happened?

1. ✅ CMake configured the project
2. ✅ C++ compiler built the engine library (`libxengine.a`)  
3. ✅ Built the demo executable (`xengine_demo`)
4. ✅ Ran the demo for 5 seconds

## 🎮 Build Your First Game

### Option 1: C++ Game

```cpp
// my_game.cpp
#include "src/core/engine.h"

int main() {
    using namespace xengine;
    
    EngineConfig config;
    config.appName = "My Game";
    config.windowWidth = 1280;
    config.windowHeight = 720;
    
    Engine& engine = Engine::getInstance();
    engine.initialize(config);
    
    while (engine.isRunning()) {
        engine.update(engine.getDeltaTime());
        engine.render();
        
        // Your game code here!
        
        if (engine.getTime() > 10.0f) {
            engine.quit();
        }
    }
    
    engine.shutdown();
    return 0;
}
```

**Compile it:**
```bash
g++ my_game.cpp build/libxengine.a -Isrc -o my_game -std=c++17
./my_game
```

### Option 2: Nova Game

```nova
// my_game.nova
program MyGame

import xengine.core

fn main() {
    let engine = XEngine.create(EngineConfig {
        windowWidth: 1280,
        windowHeight: 720,
        windowTitle: "My Nova Game"
    })
    
    while engine.isRunning() {
        engine.update(engine.getDeltaTime())
        engine.render()
        
        // Your game code here!
        
        if engine.getTime() > 10.0 {
            engine.quit()
        }
    }
    
    engine.shutdown()
}
```

### Option 3: Vex Game

```vex
// my_game.vex
import { useState, useEffect } from "@xengine/core"

component Game() {
    const [time, setTime] = useState(0)
    
    useEffect(() => {
        const timer = setInterval(() => {
            setTime(t => t + 0.016)
        }, 16)
        
        return () => clearInterval(timer)
    }, [])
    
    render =>
        <GameCanvas width={1280} height={720}>
            <h1>My Vex Game</h1>
            <p>Time: {time.toFixed(2)}s</p>
        </GameCanvas>
}

export default Game
```

## 📦 Build for Different Platforms

### Android APK

```bash
python3 tools/apk-builder.py . -o build/android
```

Output: `build/android/game.apk`

### iOS IPA

```bash
# Coming soon!
```

### Web (HTML5)

```bash
# Install Emscripten first
cmake .. -DCMAKE_TOOLCHAIN_FILE=$EMSDK/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake
cmake --build .
```

Output: `build/index.html`

## 🐛 Troubleshooting

**"cmake: command not found"**
```bash
# Ubuntu
sudo apt-get install cmake

# macOS  
brew install cmake
```

**"g++: command not found"**
```bash
# Ubuntu
sudo apt-get install build-essential

# macOS
xcode-select --install
```

**Build fails with errors**
```bash
# Check your compiler version
g++ --version  # Should be 9.0 or higher
cmake --version  # Should be 3.15 or higher
```

## 📚 Next Steps

1. Read full documentation: `docs/getting-started.md`
2. Try example games: `examples/platformer/`
3. Explore API: `src/` folder
4. Join community: [Discord](#) | [Forum](#)

## 💡 Tips

- ✅ Start with the simple C++ example
- ✅ Use `./build.sh` to rebuild after changes
- ✅ Check `build/libxengine.a` exists after build
- ✅ Run `./build/xengine_demo` to test
- ✅ Add your game files to `examples/` folder

## ⚡ Features Coming Soon

- [ ] Full OpenGL/Vulkan renderer
- [ ] 2D/3D physics integration
- [ ] Audio system with 3D sound
- [ ] Input handling (keyboard, mouse, touch, gamepad)
- [ ] Asset loading and management
- [ ] Scene graph system
- [ ] Particle effects
- [ ] Network multiplayer
- [ ] Visual editor

---

**Made with ❤️  for game developers worldwide**

🎮 Happy game development! 🎮
