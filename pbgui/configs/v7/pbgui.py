class PBGui:
    def __init__(self):
        self._version = 0
        self._enabled_on = "disabled"
        self._only_cpt = False
        self._starting_config = False
        self._market_cap = 0
        self._vol_mcap = 10.0
        self._tags = []
        self._dynamic_ignore = False
        self._notices_ignore = False
        self._note = ''
        self._backtest_div_by = 60
        self._pbgui = {
            "version": self._version,
            "enabled_on": self._enabled_on,
            "only_cpt": self._only_cpt,
            "starting_config": self._starting_config,
            "market_cap": self._market_cap,
            "vol_mcap": self._vol_mcap,
            "tags": self._tags,
            "dynamic_ignore": self._dynamic_ignore,
            "notices_ignore": self._notices_ignore,
            "note": self._note,
            "backtest_div_by": self._backtest_div_by,
        }
    
    def __repr__(self):
        return str(self._pbgui)
    
    @property
    def pbgui(self): return self._pbgui
    @pbgui.setter
    def pbgui(self, new_pbgui):
        if "version" in new_pbgui:
            self.version = new_pbgui["version"]
        if "enabled_on" in new_pbgui:
            self.enabled_on = new_pbgui["enabled_on"]
        if "only_cpt" in new_pbgui:
            self.only_cpt = new_pbgui["only_cpt"]
        if "starting_config" in new_pbgui:
            self.starting_config = new_pbgui["starting_config"]
        if "market_cap" in new_pbgui:
            self.market_cap = new_pbgui["market_cap"]
        if "vol_mcap" in new_pbgui:
            self.vol_mcap = new_pbgui["vol_mcap"]
        if "tags" in new_pbgui:
            self.tags = new_pbgui["tags"]
        if "dynamic_ignore" in new_pbgui:
            self.dynamic_ignore = new_pbgui["dynamic_ignore"]
        if "notices_ignore" in new_pbgui:
            self.notices_ignore = new_pbgui["notices_ignore"]
        if "note" in new_pbgui:
            self.note = new_pbgui["note"]
        if "backtest_div_by" in new_pbgui:
            self.backtest_div_by = new_pbgui["backtest_div_by"]

    @property
    def version(self): return self._version
    @property
    def enabled_on(self): return self._enabled_on
    @property
    def only_cpt(self): return self._only_cpt
    @property
    def starting_config(self): return self._starting_config
    @property
    def market_cap(self): return self._market_cap
    @property
    def vol_mcap(self): return self._vol_mcap
    @property
    def tags(self): return self._tags
    @property
    def dynamic_ignore(self): return self._dynamic_ignore
    @property
    def notices_ignore(self): return self._notices_ignore
    @property
    def note(self): return self._note
    @property
    def backtest_div_by(self): return self._backtest_div_by

    @version.setter
    def version(self, new_version):
        self._version = new_version
        self._pbgui["version"] = self._version
    @enabled_on.setter
    def enabled_on(self, new_enabled_on):
        self._enabled_on = new_enabled_on
        self._pbgui["enabled_on"] = self._enabled_on
    @only_cpt.setter
    def only_cpt(self, new_only_cpt):
        self._only_cpt = new_only_cpt
        self._pbgui["only_cpt"] = self._only_cpt
    @starting_config.setter
    def starting_config(self, new_starting_config):
        self._starting_config = new_starting_config
        self._pbgui["starting_config"] = self._starting_config
    @market_cap.setter
    def market_cap(self, new_market_cap):
        self._market_cap = new_market_cap
        self._pbgui["market_cap"] = self._market_cap
    @vol_mcap.setter
    def vol_mcap(self, new_vol_mcap):
        self._vol_mcap = new_vol_mcap
        self._pbgui["vol_mcap"] = self._vol_mcap
    @tags.setter
    def tags(self, new_tags):
        self._tags = new_tags
        self._pbgui["tags"] = self._tags
    @dynamic_ignore.setter
    def dynamic_ignore(self, new_dynamic_ignore):
        self._dynamic_ignore = new_dynamic_ignore
        self._pbgui["dynamic_ignore"] = self._dynamic_ignore
    @notices_ignore.setter
    def notices_ignore(self, new_notices_ignore):
        self._notices_ignore = new_notices_ignore
        self._pbgui["notices_ignore"] = self._notices_ignore
    @note.setter
    def note(self, new_note):
        self._note = new_note
        self._pbgui["note"] = self._note
    @backtest_div_by.setter
    def backtest_div_by(self, new_backtest_div_by):
        self._backtest_div_by = new_backtest_div_by
        self._pbgui["backtest_div_by"] = self._backtest_div_by
