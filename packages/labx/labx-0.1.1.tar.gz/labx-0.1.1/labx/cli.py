import sys
import requests
import curses
from io import BytesIO
import os

import subprocess

# Pastebin raw link here (make sure it's the *raw* version!)
PASTEBIN_URL = "https://pastebin.com/raw/AzFAs3EG"  # Replace with your actual link

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_json_data():
    """Fetch and return JSON data from Pastebin."""
    try:
        response = requests.get(PASTEBIN_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching JSON data: {e}")
        sys.exit(1)

def select_with_arrows(stdscr, items):
    """Render a selection menu with arrow keys using curses."""
    if not items:
        return None

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "Content"
        stdscr.addstr(1, (w - len(title)) // 2, title)

        for idx, item in enumerate(items):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(items) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, f"> {item} <")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, f"  {item}  ")

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            current_row += 1
        elif key in [10, 13]:  # ENTER key
            return items[current_row]
        elif key == ord('q'):
            sys.exit(0)

def download_file(url, file_type):
    """Download file from URL and save it as out.{file_type}. If zip, extract using tar."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
        }

        response = requests.get(url, headers=headers, allow_redirects=True, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if 'html' in content_type.lower():
            print("❌ Downloaded content is HTML, likely an error page. Aborting.")

        filename = f"out.{file_type}"

        # Save file
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✅ Downloaded file saved as '{filename}'")

        # If ZIP, extract using tar -xf
        if file_type == "zip":
            output_dir = "outfolder"
            os.makedirs(output_dir, exist_ok=True)
            try:
                subprocess.run(["tar", "-xf", filename, "-C", output_dir], check=True)
                print(f"📦 Extracted ZIP to '{output_dir}/'")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Extraction failed with tar: {e}")
            except FileNotFoundError:
                print("❌ 'tar' command not found. Make sure it's installed and in PATH.")
    except Exception as e:
        print(f"❌ Failed to download: {e}")
        sys.exit(1)

def curses_main(stdscr):
    """Main logic wrapped with curses."""
    data = get_json_data()
    available = data.get("available", [])
    if not available:
        stdscr.addstr(0, 0, "No items found.")
        stdscr.getch()
        return

    # Select Category
    categories = list({item["cat"] for item in available})
    selected_cat = select_with_arrows(stdscr, categories)
    clear_screen()

    # Select Subcategory
    subcats = list({item["subcat"] for item in available if item["cat"] == selected_cat})
    selected_subcat = select_with_arrows(stdscr, subcats)
    clear_screen()

    # Find matching item
    for item in available:
        if item["cat"] == selected_cat and item["subcat"] == selected_subcat:
            curses.endwin()
            download_file(item["content"], item["contenttype"])
            return

    print("No matching content found.")

def main():
    """Entry point of the CLI."""
    clear_screen()
    user_input = input().strip()
    if user_input != '7':
        sys.exit(0)

    try:
        curses.wrapper(curses_main)
    except KeyboardInterrupt:
        print("\nExited.")
