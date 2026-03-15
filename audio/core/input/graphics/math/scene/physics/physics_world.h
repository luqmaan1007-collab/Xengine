// xengine/src/physics/physics_world.h
// Physics System Header

#ifndef XENGINE_PHYSICS_WORLD_H
#define XENGINE_PHYSICS_WORLD_H

namespace xengine {

class PhysicsWorld {
public:
    PhysicsWorld() = default;
    ~PhysicsWorld() = default;
    
    void step(float deltaTime) {}
};

} // namespace xengine

#endif // XENGINE_PHYSICS_WORLD_H
