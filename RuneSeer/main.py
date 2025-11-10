import argparse
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

    pairs = [
        ("User", info["userHost"]),
        ("OS", info["os"]),
        ("Kernel", info["kernel"]),
        ("Shell", info["shell"]),
        ("Uptime", info["uptime"]),
        ("CPU", info["cpu"]),
        ("Memory", f"{memColor}{memUsedGB:4.1f} / {memTotalGB:4.1f} GiB"),
        ("Disk", f"{diskColor}{diskUsedGB:4.1f} / {diskTotalGB:4.1f} GiB"),
        ("Battery", info["battery"])
    ]

    lines = []
    for k, v in pairs:
        lines.append(f"{label}{k:8}{reset}: {value}{v}{reset}")
    return lines

def main():
    init(autoreset = True)

    parser = argparse.ArgumentParser(prog = "RuneSeer", description = "System fetch")
    parser.add_argument("--theme", choices = ["minimal"], default = "minimal")
    args = parser.parse_args()

    theme = getTheme(args.theme)

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

if __name__ == "__main__":
    main()