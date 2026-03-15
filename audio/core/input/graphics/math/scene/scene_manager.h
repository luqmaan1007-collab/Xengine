// xengine/src/scene/scene_manager.h
// Scene Management System Header

#ifndef XENGINE_SCENE_MANAGER_H
#define XENGINE_SCENE_MANAGER_H

namespace xengine {

class SceneManager {
public:
    SceneManager() = default;
    ~SceneManager() = default;
    
    void update(float deltaTime) {}
    void render() {}
};

} // namespace xengine

#endif // XENGINE_SCENE_MANAGER_H
