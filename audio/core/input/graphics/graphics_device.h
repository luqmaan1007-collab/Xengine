// xengine/src/graphics/graphics_device.h
// Graphics Device - Low-Level Graphics API

#ifndef XENGINE_GRAPHICS_DEVICE_H
#define XENGINE_GRAPHICS_DEVICE_H

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include "../math/vector.h"
#include "../math/matrix.h"

namespace xengine {

enum class TextureFormat {
    RGBA8,
    RGB8,
    RG8,
    R8,
    RGBA16F,
    RGB16F,
    RGBA32F,
    Depth24Stencil8,
    Depth32F,
    DXT1,  // Compressed formats
    DXT5,
    ETC2,
    ASTC,
    BC7
};

enum class TextureType {
    Texture1D,
    Texture2D,
    Texture3D,
    TextureCube
};

enum class PrimitiveType {
    Points,
    Lines,
    LineStrip,
    Triangles,
    TriangleStrip,
    TriangleFan
};

enum class BlendMode {
    None,
    Alpha,
    Additive,
    Multiply,
    Custom
};

enum class DepthFunc {
    Never,
    Less,
    Equal,
    LessOrEqual,
    Greater,
    NotEqual,
    GreaterOrEqual,
    Always
};

struct VertexAttribute {
    std::string name;
    uint32_t location;
    uint32_t size;       // Number of components (1-4)
    uint32_t offset;     // Offset in bytes
    uint32_t stride;     // Stride in bytes
};

class Shader {
public:
    virtual ~Shader() = default;
    virtual void bind() = 0;
    virtual void unbind() = 0;
    
    virtual void setInt(const std::string& name, int value) = 0;
    virtual void setFloat(const std::string& name, float value) = 0;
    virtual void setVec2(const std::string& name, const Vec2& value) = 0;
    virtual void setVec3(const std::string& name, const Vec3& value) = 0;
    virtual void setVec4(const std::string& name, const Vec4& value) = 0;
    virtual void setMat3(const std::string& name, const Mat3& value) = 0;
    virtual void setMat4(const std::string& name, const Mat4& value) = 0;
    virtual void setTexture(const std::string& name, uint32_t slot) = 0;
    
    virtual uint32_t getID() const = 0;
};

class Texture {
public:
    virtual ~Texture() = default;
    virtual void bind(uint32_t slot = 0) = 0;
    virtual void unbind() = 0;
    
    virtual uint32_t getWidth() const = 0;
    virtual uint32_t getHeight() const = 0;
    virtual uint32_t getDepth() const = 0;
    virtual TextureFormat getFormat() const = 0;
    virtual TextureType getType() const = 0;
    
    virtual void setData(const void* data, size_t size) = 0;
    virtual void generateMipmaps() = 0;
    
    virtual uint32_t getID() const = 0;
};

class VertexBuffer {
public:
    virtual ~VertexBuffer() = default;
    virtual void bind() = 0;
    virtual void unbind() = 0;
    
    virtual void setData(const void* data, size_t size) = 0;
    virtual void updateData(const void* data, size_t size, size_t offset = 0) = 0;
    
    virtual size_t getSize() const = 0;
    virtual uint32_t getID() const = 0;
};

class IndexBuffer {
public:
    virtual ~IndexBuffer() = default;
    virtual void bind() = 0;
    virtual void unbind() = 0;
    
    virtual void setData(const uint32_t* indices, size_t count) = 0;
    virtual size_t getCount() const = 0;
    
    virtual uint32_t getID() const = 0;
};

class FrameBuffer {
public:
    virtual ~FrameBuffer() = default;
    virtual void bind() = 0;
    virtual void unbind() = 0;
    
    virtual void attachColorTexture(Texture* texture, uint32_t attachment = 0) = 0;
    virtual void attachDepthTexture(Texture* texture) = 0;
    
    virtual bool isComplete() const = 0;
    virtual uint32_t getID() const = 0;
};

class GraphicsDevice {
public:
    virtual ~GraphicsDevice() = default;
    
    // Initialization
    virtual bool initialize() = 0;
    virtual void shutdown() = 0;
    
    // Frame management
    virtual void beginFrame() = 0;
    virtual void endFrame() = 0;
    virtual void present() = 0;
    
    // Clear operations
    virtual void clear(const Vec4& color) = 0;
    virtual void clearDepth(float depth = 1.0f) = 0;
    virtual void clearStencil(int stencil = 0) = 0;
    
    // Viewport
    virtual void setViewport(int x, int y, int width, int height) = 0;
    virtual void getViewport(int& x, int& y, int& width, int& height) = 0;
    
    // Resource creation
    virtual std::unique_ptr<Shader> createShader(
        const std::string& vertexSource,
        const std::string& fragmentSource
    ) = 0;
    
    virtual std::unique_ptr<Texture> createTexture(
        uint32_t width,
        uint32_t height,
        TextureFormat format,
        TextureType type = TextureType::Texture2D
    ) = 0;
    
    virtual std::unique_ptr<Texture> createTextureFromFile(
        const std::string& filepath
    ) = 0;
    
    virtual std::unique_ptr<VertexBuffer> createVertexBuffer(
        const void* data,
        size_t size
    ) = 0;
    
    virtual std::unique_ptr<IndexBuffer> createIndexBuffer(
        const uint32_t* indices,
        size_t count
    ) = 0;
    
    virtual std::unique_ptr<FrameBuffer> createFrameBuffer(
        uint32_t width,
        uint32_t height
    ) = 0;
    
    // Drawing
    virtual void draw(
        PrimitiveType primitive,
        uint32_t vertexCount,
        uint32_t startVertex = 0
    ) = 0;
    
    virtual void drawIndexed(
        PrimitiveType primitive,
        uint32_t indexCount,
        uint32_t startIndex = 0
    ) = 0;
    
    virtual void drawInstanced(
        PrimitiveType primitive,
        uint32_t vertexCount,
        uint32_t instanceCount,
        uint32_t startVertex = 0
    ) = 0;
    
    // State management
    virtual void setBlendMode(BlendMode mode) = 0;
    virtual void setDepthTest(bool enabled) = 0;
    virtual void setDepthFunc(DepthFunc func) = 0;
    virtual void setDepthWrite(bool enabled) = 0;
    virtual void setCullFace(bool enabled) = 0;
    virtual void setWireframe(bool enabled) = 0;
    
    // Queries
    virtual std::string getVendor() const = 0;
    virtual std::string getRenderer() const = 0;
    virtual std::string getVersion() const = 0;
    virtual int getMaxTextureSize() const = 0;
    virtual int getMaxTextureUnits() const = 0;
};

} // namespace xengine

#endif // XENGINE_GRAPHICS_DEVICE_H
