import subprocess, winreg, platform, os

def get_reg(path, name, root=winreg.HKEY_LOCAL_MACHINE):
    try:
        key = winreg.OpenKey(root, path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return value
    except: return None

def set_reg(path, name, value, root=winreg.HKEY_LOCAL_MACHINE, val_type=winreg.REG_DWORD):
    try:
        key = winreg.CreateKeyEx(root, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, val_type, value)
        winreg.CloseKey(key)
        return True
    except: return False

def run_optimization():
    stats = {"optimal": 0, "fixed": 0, "failed": 0}
    
    def log_status(condition, action_callback, label):
        if condition:
            print(f"[ Optimal ] {label}")
            stats["optimal"] += 1
        else:
            success = action_callback()
            if success:
                print(f"[ Fixed   ] {label}")
                stats["fixed"] += 1
            else:
                print(f"[ Failed  ] {label}")
                stats["failed"] += 1

    print(f"--- CS2 Optimization Tool | {platform.processor()} ---")

    # 1. Game Mode
    # https://learn.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/microsoft-windows-shell-setup-gamebar
    gm_key = r"Software\Microsoft\GameBar"
    log_status(get_reg(gm_key, "AllowAutoGameMode", winreg.HKEY_CURRENT_USER) == 1,
               lambda: set_reg(gm_key, "AllowAutoGameMode", 1, winreg.HKEY_CURRENT_USER), "Game Mode")

    # 2. HAGS - Hardware-Accelerated GPU Scheduling
    # https://devblogs.microsoft.com/directx/hardware-accelerated-gpu-scheduling/
    hags_key = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
    log_status(get_reg(hags_key, "HwSchMode") == 2,
               lambda: set_reg(hags_key, "HwSchMode", 2), "Hardware GPU Scheduling")

    # 3. High Performance GPU Profile
    # https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range
    gpu_key = r"Software\Microsoft\DirectX\UserGpuPreferences"
    log_status(get_reg(gpu_key, "cs2.exe", winreg.HKEY_CURRENT_USER) == "GpuPreference=2;",
               lambda: set_reg(gpu_key, "cs2.exe", "GpuPreference=2;", winreg.HKEY_CURRENT_USER, winreg.REG_SZ), "GPU High-Perf Profile")

    # 4. Disable Memory Integrity (Core Isolation)
    # https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity
    mi_key = r"SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity"
    log_status(get_reg(mi_key, "Enabled") == 0,
               lambda: set_reg(mi_key, "Enabled", 0), "Memory Integrity")

    # 5. Power Plan - Ultimate Performance
    # https://learn.microsoft.com/en-us/windows-hardware/customize/power-settings/configure-power-settings
    res = subprocess.run("powercfg /getactivescheme", shell=True, capture_output=True, text=True)
    is_ult = "e9a42b02-d5df-448d-aa00-03f14749eb61" in res.stdout.lower()
    log_status(is_ult, lambda: subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 && powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True).returncode == 0, "Ultimate Power Plan")

    # 6. Disable Microsoft Startup Apps
    # https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys
    run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    ms_apps = ["OneDrive", "com.squirrel.Teams.Teams", "Skype", "CortanaStartupId"]
    def disable_ms_apps():
        for app in ms_apps:
            if get_reg(run_key, app, winreg.HKEY_CURRENT_USER) is not None:
                set_reg(run_key, app, "", winreg.HKEY_CURRENT_USER, winreg.REG_SZ)
        return True
    ms_optimal = all(get_reg(run_key, app, winreg.HKEY_CURRENT_USER) in [None, ""] for app in ms_apps)
    log_status(ms_optimal, disable_ms_apps, "Microsoft Startup Apps")

    # 7. Multimedia Priority
    # https://learn.microsoft.com/en-us/windows/win32/procthread/multimedia-class-scheduler-service
    mp_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games"
    mp_optimal = get_reg(mp_key, "GPU Priority") == 8 and get_reg(mp_key, "Priority") == 6
    log_status(mp_optimal, lambda: set_reg(mp_key, "GPU Priority", 8) and set_reg(mp_key, "Priority", 6) and set_reg(mp_key, "Scheduling Category", "High", val_type=winreg.REG_SZ), "Multimedia Priority")

    # 8. CS2 CPU Priority
    # https://learn.microsoft.com/en-us/windows/win32/procthread/scheduling-priorities
    cp_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\cs2.exe\PerfOptions"
    log_status(get_reg(cp_key, "CpuPriorityClass") == 3,
               lambda: set_reg(cp_key, "CpuPriorityClass", 3), "CS2 CPU Priority")

    # 9. Fullscreen Optimizations
    # https://devblogs.microsoft.com/directx/demystifying-full-screen-optimizations/
    fso_key = r"System\GameConfigStore"
    log_status(get_reg(fso_key, "GameDVR_FSEBehavior", winreg.HKEY_CURRENT_USER) == 2,
               lambda: set_reg(fso_key, "GameDVR_FSEBehavior", 2, winreg.HKEY_CURRENT_USER), "Fullscreen Optimizations")

    # 10. Mouse Acceleration
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa
    ma_key = r"Control Panel\Mouse"
    ma_opt = get_reg(ma_key, "MouseSpeed", winreg.HKEY_CURRENT_USER) == "0"
    log_status(ma_opt, lambda: set_reg(ma_key, "MouseSpeed", "0", winreg.HKEY_CURRENT_USER, winreg.REG_SZ) and set_reg(ma_key, "MouseThreshold1", "0", winreg.HKEY_CURRENT_USER, winreg.REG_SZ) and set_reg(ma_key, "MouseThreshold2", "0", winreg.HKEY_CURRENT_USER, winreg.REG_SZ), "Mouse Acceleration")

    # 11. Cloudflare DNS
    # https://developers.cloudflare.com/1.1.1.1/
    dns_check = subprocess.run(["powershell", "-Command", "Get-DnsClientServerAddress | Select-Object -ExpandProperty ServerAddresses"], capture_output=True, text=True)
    log_status("1.1.1.1" in dns_check.stdout, lambda: subprocess.run(["powershell", "-Command", 'Set-DnsClientServerAddress -InterfaceAlias "*" -ServerAddresses ("1.1.1.1","1.0.0.1")'], capture_output=True).returncode == 0, "Cloudflare DNS")
    subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)

    print(f"\n--- Summary: {stats['optimal']} Optimal, {stats['fixed']} Fixed, {stats['failed']} Failed ---")
    if stats['fixed'] > 0: print("Reboot required to apply changes.")

if __name__ == "__main__":
    run_optimization()
