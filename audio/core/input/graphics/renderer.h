// xengine/src/graphics/renderer.h
// Renderer System Header

#ifndef XENGINE_RENDERER_H
#define XENGINE_RENDERER_H

namespace xengine {

class Renderer {
public:
    Renderer() = default;
    ~Renderer() = default;
    
    void beginFrame() {}
    void endFrame() {}
    void present() {}
};

} // namespace xengine

#endif // XENGINE_RENDERER_H
