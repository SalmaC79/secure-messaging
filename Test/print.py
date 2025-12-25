from colorama import init, Fore, Back, Style

init(autoreset=True)

# -----------------------------
# Foreground colors
# -----------------------------
print(Fore.RED + "❌ Error message")
print(Fore.GREEN + "✔ Success message")
print(Fore.YELLOW + "⚠ Warning message")
print(Fore.CYAN + "📬 Info message")
print(Fore.MAGENTA + "🔮 Fun/magenta message")
print(Fore.BLUE + "💧 Blue info or tip")

# -----------------------------
# Background colors
# -----------------------------
print(Back.RED + "❌ Error with red background")
print(Back.GREEN + "✔ Success with green background")
print(Back.YELLOW + "⚠ Warning with yellow background")
print(Back.CYAN + "📬 Info with cyan background")

# -----------------------------
# Styles
# -----------------------------
print(Style.BRIGHT + "Bright text")
print("Bright text")
print(Style.DIM + "Dim text")
print(Style.NORMAL + "Normal text")
print(Fore.MAGENTA + Style.BRIGHT + "Fancy magenta bold text")
print(Fore.YELLOW + Style.DIM + "Dim yellow text")

# -----------------------------
# Combine Fore + Back + Style
# -----------------------------
print(Fore.WHITE + Back.RED + Style.BRIGHT + "❌ Bold white on red background")
print(Fore.BLACK + Back.GREEN + Style.BRIGHT + "✔ Bold black on green background")
print(Fore.CYAN + Back.MAGENTA + Style.DIM + "📌 Dim cyan on magenta")
