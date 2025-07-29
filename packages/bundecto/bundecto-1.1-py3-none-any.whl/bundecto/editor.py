import curses
import os
import signal

VERSION = "1.1"  # X.Y scheme


class BundectoApp:
    def __init__(self, filename=None, readonly=False, allow_raw=True):
        self.filename = filename
        self.buffer = TextBuffer()
        self.ui = EditorUI()
        self.running = True
        self.last_key = None
        self.show_debug = False
        self.show_help = False
        self.readonly = readonly

        signal.signal(signal.SIGINT, signal.SIG_IGN)

        if allow_raw:
            os.system("stty -ixon")

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.ui.init_screen(stdscr)
        self.buffer.init_screen(stdscr)

        if self.filename:
            self.buffer.load_file(self.filename)

        while self.running:
            self.ui.draw(
                self.buffer,
                self.filename,
                self.last_key,
                self.show_debug,
                self.show_help,
            )

            key = stdscr.getch()

            self.last_key = key
            self.handle_key(key)

    def handle_key(self, key):
        if key == 24:  # Ctrl+X
            if self.buffer.modified:
                if self.ui.are_you_sure("Save Modified Buffer?"):
                    if not self.filename:
                        self.ui.stdscr.clear()
                        self.ui.stdscr.refresh()
                        self.ui.draw(
                            self.buffer,
                            self.filename,
                            self.last_key,
                            self.show_debug,
                            self.show_help,
                        )
                        self.filename = self.ui.prompt_filename()
                    if self.filename:
                        self.buffer.save_file(self.filename)
                curses.curs_set(0)
            self.running = False
        elif key == 15:  # Ctrl+O
            self.filename = self.ui.prompt_filename()
            self.buffer.save_file(self.filename)
        elif key == 19:  # Ctrl+S
            if not self.readonly:
                if not self.filename:
                    self.filename = self.ui.prompt_filename()
                if self.filename:
                    self.buffer.save_file(self.filename)
        elif key == 7:  # Ctrl+G -> toggle debug
            self.show_debug = not self.show_debug
        elif key == 8:  # Ctrl+H -> show help
            self.show_help = not self.show_help
        else:
            self.buffer.handle_input(key)


class TextBuffer:
    def init_screen(self, stdscr: curses.window):
        self.stdscr = stdscr

    def __init__(self):
        self.lines = [""]
        self.cursor_x = 0
        self.cursor_y = 0
        self.top_line = 0
        self.modified = False
        self.left_col = 0
        self.stdscr = None

    def load_file(self, path):
        try:
            with open(path, "r") as f:
                self.lines = f.read().splitlines() or [""]
        except FileNotFoundError:
            self.lines = [""]
        self.modified = False

    def save_file(self, path):
        with open(path, "w") as f:
            f.write("\n".join(self.lines))
        self.modified = False

    def handle_input(self, key):
        if key in (curses.KEY_BACKSPACE, 127, curses.KEY_ENTER, 10, 13) or (
            32 <= key <= 126
        ):
            self.modified = True

        if key in (curses.KEY_BACKSPACE, 127):
            self._backspace()
        elif key in (curses.KEY_ENTER, 10, 13):
            self._newline()
        elif 32 <= key <= 126:
            self._insert_char(chr(key))
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(self.cursor_x - 1, 0)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.cursor_x + 1, len(self.lines[self.cursor_y]))
        elif key == curses.KEY_UP:
            self.cursor_y = max(self.cursor_y - 1, 0)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.cursor_y + 1, len(self.lines) - 1)
        elif key == curses.KEY_DC:  # Delete key
            if self.cursor_x < len(self.lines[self.cursor_y]):
                line = self.lines[self.cursor_y]
                self.lines[self.cursor_y] = (
                    line[: self.cursor_x] + line[self.cursor_x + 1 :]
                )
            elif self.cursor_y < len(self.lines) - 1:
                self.lines[self.cursor_y] += self.lines[self.cursor_y + 1]
                del self.lines[self.cursor_y + 1]
        elif key == curses.KEY_HOME:  # Home key
            self.cursor_x = 0
        elif key == curses.KEY_END:  # End key
            self.cursor_x = len(self.lines[self.cursor_y])
        elif key == 554:  # Ctrl+Left
            if self.cursor_x > 0:
                while (
                    self.cursor_x > 0
                    and self.lines[self.cursor_y][self.cursor_x - 1] in " \t"
                ):
                    self.cursor_x -= 1
                while (
                    self.cursor_x > 0
                    and self.lines[self.cursor_y][self.cursor_x - 1].isalnum()
                ):
                    self.cursor_x -= 1
        elif key == 569:  # Ctrl+Right
            if self.cursor_x < len(self.lines[self.cursor_y]):
                while (
                    self.cursor_x < len(self.lines[self.cursor_y])
                    and self.lines[self.cursor_y][self.cursor_x] in " \t"
                ):
                    self.cursor_x += 1
                while (
                    self.cursor_x < len(self.lines[self.cursor_y])
                    and self.lines[self.cursor_y][self.cursor_x].isalnum()
                ):
                    self.cursor_x += 1
        elif key == 383:  # Shift+Delete
            line = self.lines[self.cursor_y]
            start = self.cursor_x
            i = start

            while i < len(line) and line[i] in " \t":
                i += 1
            while i < len(line) and line[i].isalnum():
                i += 1

            self.lines[self.cursor_y] = line[:start] + line[i:]
        elif key == 4:  # Shift+Backspace and Ctrl+D
            if self.cursor_x > 0:
                while (
                    self.cursor_x > 0
                    and self.lines[self.cursor_y][self.cursor_x - 1] in " \t"
                ):
                    self.cursor_x -= 1
                while (
                    self.cursor_x > 0
                    and self.lines[self.cursor_y][self.cursor_x - 1].isalnum()
                ):
                    self.lines[self.cursor_y] = (
                        self.lines[self.cursor_y][: self.cursor_x - 1]
                        + self.lines[self.cursor_y][self.cursor_x :]
                    )
                    self.cursor_x -= 1
        elif key == 9:  # Tab
            tab_spaces = 4
            self.lines[self.cursor_y] = (
                self.lines[self.cursor_y][: self.cursor_x]
                + " " * tab_spaces
                + self.lines[self.cursor_y][self.cursor_x :]
            )
            self.cursor_x += tab_spaces
        elif key == 353:  # Shift+Tab
            indent_spaces = 4

            current_line = self.lines[self.cursor_y]

            if self.cursor_x >= indent_spaces and current_line[
                : self.cursor_x
            ].startswith(" " * indent_spaces):
                self.lines[self.cursor_y] = current_line[indent_spaces:]
                self.cursor_x -= indent_spaces
            elif self.cursor_x < indent_spaces:
                self.cursor_x = 0

        screen_height, screen_width = self.stdscr.getmaxyx()

        self._adjust_scroll(screen_height, screen_width)

    def _adjust_scroll(self, screen_height=24, screen_width=80):
        view_height = screen_height - 1  # reserve last line
        view_width = screen_width - 2  # room for < > indicators

        # Vertical scroll
        if self.cursor_y < self.top_line:
            self.top_line = self.cursor_y
        elif self.cursor_y >= self.top_line + view_height:
            self.top_line = self.cursor_y - view_height + 1

        # Horizontal scroll
        if self.cursor_x < self.left_col:
            self.left_col = self.cursor_x
        elif self.cursor_x >= self.left_col + view_width:
            self.left_col = self.cursor_x - view_width + 1

    def _insert_char(self, char):
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[: self.cursor_x] + char + line[self.cursor_x :]
        self.cursor_x += 1

    def _newline(self):
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[: self.cursor_x]
        self.lines.insert(self.cursor_y + 1, line[self.cursor_x :])
        self.cursor_y += 1
        self.cursor_x = 0

    def _backspace(self):
        if self.cursor_x > 0:
            line = self.lines[self.cursor_y]
            self.lines[self.cursor_y] = (
                line[: self.cursor_x - 1] + line[self.cursor_x :]
            )
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            prev_line = self.lines[self.cursor_y - 1]
            self.cursor_x = len(prev_line)
            self.lines[self.cursor_y - 1] += self.lines[self.cursor_y]
            del self.lines[self.cursor_y]
            self.cursor_y -= 1


class EditorUI:
    def init_screen(self, stdscr: curses.window):
        self.stdscr = stdscr
        curses.curs_set(1)
        curses.use_default_colors()
        self.height, self.width = self.stdscr.getmaxyx()

    def padx(self, string, width, lextra="", rextra=""):
        side_space = max(0, width - (len(lextra) * 2) - len(string) - (len(rextra) * 2))
        left_pad = side_space // 2
        right_pad = side_space - left_pad
        return f"{lextra}{' ' * left_pad}{string}{' ' * right_pad}{rextra}"

    def draw(self, buffer, filename, last_key, show_debug, show_help):
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()

        visible_lines = buffer.lines[
            buffer.top_line : buffer.top_line + self.height - 1
        ]
        for idx, line in enumerate(visible_lines):
            y = idx
            x_offset = buffer.left_col
            view_width = self.width - 2  # leave space for indicators

            # Extract visible segment
            text_segment = line[x_offset : x_offset + view_width]

            # Add left/right cut indicators
            left_char = "<" if x_offset > 0 else " "
            right_char = ">" if len(line) > x_offset + view_width else " "

            self.stdscr.addstr(
                y, 0, left_char, curses.A_REVERSE if left_char != " " else 0
            )
            self.stdscr.addstr(y, 1, text_segment)
            self.stdscr.addstr(
                y,
                self.width - 1,
                right_char,
                curses.A_REVERSE if right_char != " " else 0,
            )

        mod_indicator = " *" if buffer.modified else ""

        left_side = f"  Bundecto {VERSION}"

        fn_str = f"{filename or 'New Buffer'}{mod_indicator}"
        pad_str = self.padx(fn_str, self.width, lextra=left_side)

        footer = f"{pad_str}"

        footer = footer[: self.width - 1].ljust(self.width - 1)

        self.stdscr.addstr(self.height - 1, 0, footer, curses.A_REVERSE)

        # Move cursor (adjust for scroll)
        visible_y = buffer.cursor_y - buffer.top_line
        visible_x = buffer.cursor_x - buffer.left_col + 1  # +1 for left indicator

        if 0 <= visible_y < self.height - 1 and 1 <= visible_x < self.width - 1:
            self.stdscr.move(visible_y, visible_x)

        self.stdscr.refresh()

        if show_debug:
            self.draw_debug_popup(self.height, self.width, buffer, filename, last_key)

            if 0 <= visible_y < self.height - 1 and 1 <= visible_x < self.width - 1:
                self.stdscr.move(visible_y, visible_x)

        if show_help:
            self.draw_help_popup(self.height, self.width)

            if 0 <= visible_y < self.height - 1 and 1 <= visible_x < self.width - 1:
                self.stdscr.move(visible_y, visible_x)

    def format_key(self, key):
        if 32 <= key <= 126:
            key_repr = repr(chr(key))
        elif 1 <= key <= 26:
            key_repr = f"'Ctrl+{chr(key + 64)}'"  # Ctrl+A to Ctrl+Z
        else:
            key_repr = f"'Non-printable {key}'"

        return f"{key_repr}"

    def draw_debug_popup(self, h, w, buffer, filename, last_key):
        popup_h, popup_w = 10, 40
        start_y = (h - popup_h) // 2 + (h // 2 - popup_h // 2) - 1
        start_x = (w - popup_w) // 2 + (w // 2 - popup_w // 2) - 1
        win = curses.newwin(popup_h, popup_w, start_y, start_x)
        win.border()

        info = [
            "[ Debug Info ]",
            f"screen={h}x{w}",
            f"cursorY={buffer.cursor_y}",
            f"cursorX={buffer.cursor_x}",
            f"cursorPos=({buffer.cursor_y},{buffer.cursor_x})"
            f"topLine={buffer.top_line}",
            f"lines={len(buffer.lines)}",
            f"lastKey=({hex(last_key)}, {self.format_key(last_key)})",
            f"modified={'yes' if buffer.modified else 'no'}",
            f"filename={filename or 'unsaved'}",
        ]

        for i, line in enumerate(info):
            win.addstr(
                i,
                (
                    2
                    if line[: popup_w - 4] != "[ Debug Info ]"
                    else (popup_w - len(line)) // 2
                ),
                line[: popup_w - 4],
            )

        win.refresh()

    def draw_help_popup(self, h, w):
        popup_h, popup_w = min(13, h - 2), min(44, w - 2)
        if popup_h < 13 or popup_w < 44:
            return
        start_y = (h - popup_h) // 2
        start_x = (w - popup_w) // 2
        win = curses.newwin(popup_h, popup_w, start_y, start_x)
        win.border()

        help_text = [
            "[ Bundecto Help ]",
            "",
            "Ctrl+X      - Exit",
            "Ctrl+S      - Save",
            "Ctrl+O      - Save As",
            "Ctrl+D      - Delete Clump (Right)",
            "Shift+Del   - Delete Clump (Left)",
            "Tab         - Indent",
            "Shift+Tab   - Unindent",
            "Ctrl+G      - Toggle Debug",
            "Ctrl+H      - Show Help",
            "",
        ]

        for i, line in enumerate(help_text):
            win.addstr(
                i,
                (
                    5
                    if line[: popup_w - 4] != "[ Bundecto Help ]"
                    else (popup_w - len(line)) // 2
                ),
                line[: popup_w - 2],
            )

        win.refresh()

    def are_you_sure(self, message="Are you sure?"):
        width = max(len(message) + 4, 20)
        height = 7
        start_y = (self.height - height) // 2
        start_x = (self.width - width) // 2
        curses.curs_set(0)

        win = curses.newwin(height, width, start_y, start_x)
        win.keypad(True)
        win.box()

        # Message
        win.addstr(2, 2, message)

        buttons = [" Yes ", " No "]
        current = 0

        def draw_buttons():
            for i, btn in enumerate(buttons):
                x = (width // 4) * (i * 2 + 1) - len(btn) // 2
                if i == current:
                    win.attron(curses.A_REVERSE)
                    win.addstr(height - 3, x, btn)
                    win.attroff(curses.A_REVERSE)
                else:
                    win.addstr(height - 3, x, btn)

        while True:
            draw_buttons()
            win.refresh()
            key = win.getch()

            if key in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                current = (current + 1) % 2
            elif key in [ord("y"), ord("Y")] and current == 0:
                return True
            elif key in [ord("n"), ord("N")] and current == 1:
                return False
            elif key in [curses.KEY_ENTER, 10, 13]:
                return current == 0
            elif key == 27:  # ESC key cancels
                return False

    def prompt_filename(self):
        popup_h, popup_w = 3, self.width - 2
        start_y = (self.height - popup_h) // 2
        start_x = (self.width - popup_w) // 2
        win = curses.newwin(popup_h, popup_w, start_y, start_x)
        win.border()

        win.addstr(0, 2, "File Name to Write:")
        win.refresh()

        curses.echo()
        filename = win.getstr(1, 2, self.width - 4).decode("utf-8")
        curses.noecho()

        win.clear()

        self.stdscr.refresh()

        return filename


def main(filename, readonly=False, allow_raw=True):
    editor = BundectoApp(filename, readonly, allow_raw=allow_raw)
    editor.run()
