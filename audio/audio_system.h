// xengine/src/audio/audio_system.h
// Audio System Header

#ifndef XENGINE_AUDIO_SYSTEM_H
#define XENGINE_AUDIO_SYSTEM_H

namespace xengine {

class AudioSystem {
public:
    AudioSystem() = default;
    ~AudioSystem() = default;
    
    void update(float deltaTime) {}
};

} // namespace xengine

#endif // XENGINE_AUDIO_SYSTEM_H
