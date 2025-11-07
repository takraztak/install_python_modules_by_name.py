# == install_modules.py ==
# Установка модулей Python с Braille-спиннером (⣾⣽⣻⢿⡿⣟⣯⣷)
# Подробный вывод, защита от ошибок и аккуратный лог.
# takraztak edition v7

import sys
import subprocess
import threading
import itertools
import time
import traceback
import os

# --- Конфигурация -------------------------------------------------------------
alias_map = {
    "pillow": "PIL",
    "pyyaml": "yaml",
    "beautifulsoup4": "bs4",
    "opencv-python": "cv2",
    "python-dateutil": "dateutil",
    "scikit-learn": "sklearn",
    "pygame": "pygame",
}

# Braille spinner — “вращающиеся точки”
SPINNER_FRAMES = list("⣾⣽⣻⢿⡿⣟⣯⣷")
SPINNER_DELAY = 0.09
# ------------------------------------------------------------------------------


def spinner_task(stop_event, prefix=" "):
    """Отображает Braille-анимацию до остановки."""
    for frame in itertools.cycle(SPINNER_FRAMES):
        if stop_event.is_set():
            break
        print(f"\r{prefix}{frame}", end="", flush=True)
        time.sleep(SPINNER_DELAY)
    print("\r" + " " * (len(prefix) + 3) + "\r", end="", flush=True)


def install_package(pkg):
    """Устанавливает и проверяет один пакет."""
    mod = alias_map.get(pkg.lower(), pkg)
    print(f"🔹 {pkg}")

    try:
        __import__(mod)
        print(f"   ✅ Уже установлен как '{mod}'.\n")
        return
    except ImportError:
        print(f"   ⬇️  Установка '{pkg}'...\n")

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_task, args=(stop_event, "   ⏳ "))
    spinner_thread.start()

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
            capture_output=True,
            text=True,
            check=False
        )
    finally:
        stop_event.set()
        spinner_thread.join()

    if result.returncode == 0:
        print(f"   ✅ Успешно установлено: {pkg}")
        try:
            __import__(mod)
            print(f"   🧩 Импорт '{mod}' прошёл успешно.\n")
        except Exception as e:
            print(f"   ⚠️  Установлен, но не импортируется: {e}\n")
    else:
        print(f"   ❌ Ошибка установки '{pkg}' (код {result.returncode})")
        print("   ───────────────────────────────────────────────")
        print(result.stderr.strip() or result.stdout.strip())
        print("   ───────────────────────────────────────────────\n")


def main():
    if len(sys.argv) < 2:
        modules = input("📦 Введи имена модулей через пробел: ").split()
    else:
        modules = sys.argv[1:]

    print("\n📦 Проверка и установка модулей")
    print("══════════════════════════════════════════════════\n")

    start_time = time.time()

    for pkg in modules:
        try:
            install_package(pkg)
        except Exception:
            print(f"\n💥 Неожиданная ошибка при обработке '{pkg}':")
            traceback.print_exc()
            print()

    elapsed = time.time() - start_time
    print("══════════════════════════════════════════════════")
    print(f"🎯 Завершено. Обработано {len(modules)} модулей за {elapsed:.1f} сек.\n")

    os.system("pause")


if __name__ == "__main__":
    main()
