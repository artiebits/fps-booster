# CS2 FPS Booster

A Windows tool to maximize Counter-Strike 2 performance. VAC & FACEIT Safe — only standard Windows settings modified, not CS2 game files.

## Features

| Optimization | Description |
|-------------|-------------|
| Game Mode | Prioritizes CPU/GPU resources for gaming |
| Memory Integrity Disabled | Disables Core Isolation for 5-10% FPS boost |
| Ultimate Performance Power Plan | Prevents CPU from downclocking during gameplay |
| Hardware-Accelerated GPU Scheduling | Reduces CPU overhead and input latency |
| CS2 CPU Priority | Runs CS2.exe at high priority (same as `-high` launch option) |
| Multimedia Priority | Sets GPU and CPU scheduling to high priority for games |
| Fullscreen Optimizations Disabled | Disables Windows FSO for lower input latency |
| High Performance GPU Profile | Forces Windows to use dedicated GPU for CS2 |
| Microsoft Startup Apps Disabled | Stops OneDrive, Teams, Skype, Cortana from running in the background |
| Mouse Acceleration Disabled | Removes pointer acceleration for 1:1 mouse movement |
| Cloudflare DNS | Sets DNS to 1.1.1.1 for faster server lookups |

## Usage

Requirements: Windows 10/11, Python 3.7+

Run as Administrator:

```bash
python fps_booster.py
```

The script checks each setting and shows status:
- `[ Optimal ]` - Already configured
- `[ Fixed   ]` - Applied successfully
- `[ Failed  ]` - Could not apply (check permissions)

## Disclaimer

This tool changes Windows system settings. Use at your own risk.
