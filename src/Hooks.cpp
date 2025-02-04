#include "Hooks.h"
#include "Settings.h"

namespace Hooks
{
    void Install() noexcept
    {
        REL::Relocation<std::uintptr_t> SprintLimit{ RELOCATION_ID(509804, 382518) };
        REL::safe_write(SprintLimit.address(), &Settings::limit, sizeof(float));
        logger::info("Installed main update hook");
        logger::info("");
    }
} // namespace Hooks
