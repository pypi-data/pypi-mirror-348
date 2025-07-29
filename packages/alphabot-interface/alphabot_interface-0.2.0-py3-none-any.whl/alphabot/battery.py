import time

# === Battery Configuration ===
BATTERY_CAPACITY_MAH = 3500
BATTERY_VOLTAGE_V = 7.4

ACTIVE_DRAW_MA = 500     # Draw when bot is running
IDLE_DRAW_MA = 100       # Draw when bot is idle

class Battery:
    def __init__(self):
        self._start_time = time.time()
        self._last_state_change = self._start_time
        self._active_time = 0       # in minutes
        self._idle_time = 0         # in minutes
        self._is_active = False

    def activate(self):
        """
        Switch to active mode, consuming more current.
        """
        self._update_usage()
        self._is_active = True
        self._last_state_change = time.time()

    def deactivate(self):
        """
        Switch to idle mode, consuming less current.
        """
        self._update_usage()
        self._is_active = False
        self._last_state_change = time.time()

    def _update_usage(self):
        """
        Update time spent in the current state (active/idle).
        """
        now = time.time()
        elapsed = (now - self._last_state_change) / 60  # seconds to minutes
        if self._is_active:
            self._active_time += elapsed
        else:
            self._idle_time += elapsed

    def get_battery_percent(self):
        """
        Calculate battery percentage based on total consumption.
        """
        self._update_usage()  # make sure we count up to now

        used_mah = (self._active_time * ACTIVE_DRAW_MA) + (self._idle_time * IDLE_DRAW_MA)
        used_ratio = min(used_mah / BATTERY_CAPACITY_MAH, 1.0)
        percent_left = round((1 - used_ratio) * 100, 2)
        return percent_left

    def get_battery_status(self):
        """
        Returns current battery status.
        """
        percent = self.get_battery_percent()
        return {
            "percent": percent,
            "low_warning": percent < 20,
            "critical_warning": percent < 5,
            "active": self._is_active,
            "active_time_min": round(self._active_time, 2),
            "idle_time_min": round(self._idle_time, 2)
        }