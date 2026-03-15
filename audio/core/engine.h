//  xengine/src/core/engine.h
// Core Xengine Engine - Main Engine Class

#ifndef XENGINE_CORE_ENGINE_H
#define XENGINE_CORE_ENGINE_H

#include <memory>
#include <string>
#include <vector>
#include "math/vector.h"
#include "graphics/renderer.h"
#include "physics/physics_world.h"
#include "audio/audio_system.h"
#include "input/input_manager.h"
#include "scene/scene_manager.h"

namespace xengine {

enum class Platform {
    Windows,
    macOS,
    Linux,
    Android,
    iOS,
    Web,
    PlayStation5,
    XboxSeriesX,
    NintendoSwitch
};

enum class RenderAPI {
    OpenGL,
    Vulkan,
    Metal,
    DirectX12,
    WebGL,
    WebGPU
};

struct EngineConfig {
    std::string appName = "Xengine Game";
    int windowWidth = 1280;
    int windowHeight = 720;
    bool fullscreen = false;
    bool vsync = true;
    RenderAPI renderAPI = RenderAPI::OpenGL;
    int targetFPS = 60;
    bool enablePhysics = true;
    bool enableAudio = true;
    bool enableNetworking = false;
};

class Engine {
public:
    static Engine& getInstance();
    
    // Initialization
    bool initialize(const EngineConfig& config);
    void shutdown();
    
    // Main loop
    void run();
    bool isRunning() const;
    void quit();
    
    // Frame management
    void update(float deltaTime);
    void fixedUpdate(float fixedDeltaTime);
    void render();
    
    // Module access
    Renderer* getRenderer();
    PhysicsWorld* getPhysicsWorld();
    AudioSystem* getAudioSystem();
    InputManager* getInputManager();
    SceneManager* getSceneManager();
    
    // Platform info
    Platform getPlatform() const;
    const std::string& getPlatformName() const;
    
    // Time management
    float getDeltaTime() const;
    float getTime() const;
    float getFPS() const;
    
    // Window management
    void* getWindow();
    void setWindowTitle(const std::string& title);
    void setWindowSize(int width, int height);
    void setFullscreen(bool fullscreen);
    
private:
    Engine() = default;
    ~Engine() = default;
    Engine(const Engine&) = delete;
    Engine& operator=(const Engine&) = delete;
    
    bool m_running = false;
    float m_deltaTime = 0.0f;
    float m_time = 0.0f;
    float m_accumulator = 0.0f;
    float m_fixedTimeStep = 1.0f / 60.0f;
    uint64_t m_frameCount = 0;
    Platform m_platform;
    EngineConfig m_config;
    
    std::unique_ptr<Renderer> m_renderer;
    std::unique_ptr<PhysicsWorld> m_physicsWorld;
    std::unique_ptr<AudioSystem> m_audioSystem;
    std::unique_ptr<InputManager> m_inputManager;
    std::unique_ptr<SceneManager> m_sceneManager;
};

} // namespace xengine

#endif // XENGINE_CORE_ENGINE_H
