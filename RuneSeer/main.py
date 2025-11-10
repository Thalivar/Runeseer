import argparse, os, time
from itertools import zip_longest
from colorama import init, Style, Fore
from systemInfo import getSystemInfo
from theme import getTheme

def colorUsage(pct, valueColor):
    pct = max(0, min(100, pct))
    if pct > 90:
        return Fore.RED
    elif pct > 70:
        return Fore.YELLOW
    else:
        return valueColor

def bar(pct, width = 20, fill = "#", empty = "-"):
    pct = max(0, min(100, pct))
    filled = int(width * pct / 100)
    return fill * filled + empty * (width - filled)

def toGiB(bytes):
    return bytes / (1024 ** 3)

def formatLines(info, theme):
    label = theme["label"]
    value = theme["value"]
    reset = Style.RESET_ALL

    memUsedGB = info["memoryUsed"] / (1024 ** 3)
    memTotalGB = info["memoryTotal"] / (1024 ** 3)
    memPct = (memUsedGB / memTotalGB * 100) if memTotalGB > 0 else 0
    memColor = colorUsage(memPct, value)

    diskUsedGB = info["diskUsed"] / (1024 ** 3)
    diskTotalGB = info["diskTotal"] / (1024 ** 3)
    diskPct = (diskUsedGB / diskTotalGB * 100) if diskTotalGB > 0 else 0
    diskColor = colorUsage(diskPct, value)

    cpuPct = info.get("cpuUsage", 0)
    cpuColor = colorUsage(cpuPct, value)
    cpuBar = bar(cpuPct)

    netSentGB = toGiB(info["netSent"])
    netRecvGB = toGiB(info["netRecv"])

    battPct = info.get("batteryPct", None)
    if battPct is not None:
        battColor = colorUsage(battPct, value)
        battBar = bar(battPct)
        battDisplay = f"{battColor}{battPct:4.0f}% {battBar}{reset}"
    else:
        battDisplay = info.get("battery", "N/A")

    pairs = [
        ("User", info["userHost"]),
        ("OS", info["os"]),
        ("Kernel", info["kernel"]),
        ("Shell", info["shell"]),
        ("Uptime", info["uptime"]),
        ("CPU Model", info["cpu"]),
        ("CPU", f"{cpuColor}{cpuPct:4.1f}% {cpuBar}{reset}"),
        ("Memory", f"{memColor}{memUsedGB:4.1f} / {memTotalGB:4.1f} GiB"),
        ("Disk", f"{diskColor}{diskUsedGB:4.1f} / {diskTotalGB:4.1f} GiB"),
        ("Battery", battDisplay),
        ("Net Sent", f"{netSentGB:4.2f} GiB"),
        ("Net Recv", f"{netRecvGB:4.2f} GiB"),
    ]

    lines = []
    for k, v in pairs:
        lines.append(f"{label}{k:8}{reset}: {value}{v}{reset}")
    return lines

def drawOnce( theme):
    accent = theme["accent"]
    reset = Style.RESET_ALL
    title = f"{accent}{theme['name']}{reset}"
    subtitle = f"{theme['value']}{theme['subtitle']}{reset}"
    print(f"{title} {subtitle}\n")

    info = getSystemInfo()
    infoLines = formatLines(info, theme)
    logoLines = theme["ascii"].strip("\n").splitlines()
    padding = theme["padding"]

    for art, line in zip_longest(logoLines, infoLines, fillvalue = ""):
        left = f"{theme['accent']}{art}{reset}"
        print(f"{left:<{padding}} {line}")

def main():
    init(autoreset = True)

    parser = argparse.ArgumentParser(prog = "RuneSeer", description = "System fetch")
    parser.add_argument("--theme", choices = ["minimal", "cat", "dragon"], default = "minimal")
    parser.add_argument("--live", action = "store_true", help = "Enable live mode (auto-refresh)")
    parser.add_argument("--interval", type = float, default = 1.0, help = "Refresh interval in seconds for live mode")
    args = parser.parse_args()

    theme = getTheme(args.theme)
    accent = theme["accent"]
    reset = Style.RESET_ALL

    if args.live:
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                drawOnce(theme)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            pass
    else:
        drawOnce(theme)

if __name__ == "__main__":
    main()