from .long import Long
from .short import Short


class Bot:
    def __init__(self):
        self._long = Long()
        self._short = Short()
        self._bot = {
            "long": self._long._long,
            "short": self._short._short
        }

    def __repr__(self):
        return str(self._bot)

    @property
    def bot(self): return self._bot

    @bot.setter
    def bot(self, new_bot):
        if "long" in new_bot:
            self.long = new_bot["long"]
        if "short" in new_bot:
            self.short = new_bot["short"]

    @property
    def long(self): return self._long

    @property
    def short(self): return self._short

    @long.setter
    def long(self, new_long):
        self._long.long = new_long
        self._bot["long"] = self._long.long

    @short.setter
    def short(self, new_short):
        self._short.short = new_short
        self._bot["short"] = self._short.short

    # UI helpers -------------------------------------------------------------
    def edit(self):
        """Render the Streamlit editor for long/short configuration."""
        from pbgui.ui import bot_ui
        bot_ui.edit(self)

    def edit_cf(self):
        """Render the copy-from editor (used in config factory screens)."""
        from pbgui.ui import bot_ui
        bot_ui.edit_cf(self)

    def edit_co(self):
        """Render the coin-override editor."""
        from pbgui.ui import bot_ui
        bot_ui.edit_co(self)
