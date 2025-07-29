import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Führe debootstrap mit gegebenen Parametern aus."
    )
    parser.add_argument('-a', '--arch', required=True, help='Zielarchitektur (z. B. arm64, amd64)')
    parser.add_argument('-r', '--release', required=True, help='Codename des Releases (z. B. noble)')
    parser.add_argument('-o', '--output', required=True, help='Zielverzeichnis für Rootfs')
    parser.add_argument('-u', '--url', required=True, help='Spiegel-URL (z. B. http://archive.ubuntu.com/ubuntu)')

    args = parser.parse_args()

    cmd = [
        "sudo",
        "debootstrap",
        f"--arch={args.arch}",
        args.release,
        args.output,
        args.url
    ]

    print(f"[INFO] Führe aus: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] debootstrap fehlgeschlagen: {e}", file=sys.stderr)
        sys.exit(e.returncode)
