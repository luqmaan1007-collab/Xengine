// examples/simple/main.cpp
// Simple Working Xengine Example

#include "../../src/core/engine.h"
#include <iostream>

int main() {
    using namespace xengine;
    
    std::cout << "\n";
    std::cout << "╔═══════════════════════════════════╗\n";
    std::cout << "║   XENGINE SIMPLE DEMO GAME        ║\n";
    std::cout << "╚═══════════════════════════════════╝\n";
    std::cout << "\n";
    
    // Create engine configuration
    EngineConfig config;
    config.appName = "Xengine Simple Demo";
    config.windowWidth = 1280;
    config.windowHeight = 720;
    config.fullscreen = false;
    config.vsync = true;
    config.targetFPS = 60;
    config.renderAPI = RenderAPI::OpenGL;
    config.enablePhysics = true;
    config.enableAudio = true;
    config.enableNetworking = false;
    
    // Get engine instance
    Engine& engine = Engine::getInstance();
    
    // Initialize engine
    if (!engine.initialize(config)) {
        std::cerr << "Failed to initialize engine!" << std::endl;
        return 1;
    }
    
    std::cout << "\nPress Ctrl+C to quit...\n" << std::endl;
    
    // Simple game loop counter
    int frameCount = 0;
    float timeElapsed = 0.0f;
    
    // Main game loop
    while (engine.isRunning()) {
        float deltaTime = engine.getDeltaTime();
        timeElapsed += deltaTime;
        frameCount++;
        
        // Print FPS every second
        if (timeElapsed >= 1.0f) {
            std::cout << "FPS: " << frameCount << " | Delta: " 
                      << (1000.0f / frameCount) << "ms" << std::endl;
            frameCount = 0;
            timeElapsed = 0.0f;
        }
        
        // Update engine (this handles game loop)
        engine.update(deltaTime);
        engine.render();
        
        // Quit after 5 seconds for demo
        if (engine.getTime() >= 5.0f) {
            std::cout << "\nDemo complete after " << engine.getTime() 
                      << " seconds!" << std::endl;
            engine.quit();
        }
    }
    
    // Shutdown
    engine.shutdown();
    
    std::cout << "\n✓ Demo finished successfully!\n" << std::endl;
    
    return 0;
}
