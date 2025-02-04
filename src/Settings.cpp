#include "Settings.h"

void Settings::LoadSettings() noexcept
{
    logger::info("Loading settings");

    CSimpleIniA ini;

    ini.SetUnicode();
    ini.LoadFile(R"(.\Data\SKSE\Plugins\SprintStutteringFix.ini)");

    // Load settings
    limit     = static_cast<float>(ini.GetDoubleValue("General", "fSpeedLimit"));

    logger::info("Loaded settings");
    logger::info("\tfSpeed limit = {}", limit);
    logger::info("");
}
