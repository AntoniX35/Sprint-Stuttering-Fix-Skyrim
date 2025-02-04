#pragma once

class Settings
{
public:
    static void LoadSettings() noexcept;

    inline static float limit{ 1100.0f };
};
