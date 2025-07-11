=============================
pibooth-date-folder Plugin v1.3.0
=============================

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/pibooth-date-folder.svg
   :target: https://pypi.org/project/pibooth-date-folder
.. |PypiVersion| image:: https://img.shields.io/pypi/v/pibooth-date-folder.svg
   :target: https://pypi.org/project/pibooth-date-folder

**pibooth-date-folder** v1.3.0 is a PiBooth plugin that
organizes photos into per-date folders with a configurable
split time, and supports multiple quoted base directories.

.. contents::
   :local:

Requirements
------------
- Python 3.6+
- PiBooth 2.8 or later

Installation
------------
Run:

    pip install pibooth-date-folder

No edits to your `pibooth.cfg` are needed; PiBooth will auto-discover the plugin.

Configuration
-------------
On first launch, this plugin adds a `[DATE_FOLDER]` section to your
`~/.config/pibooth/pibooth.cfg`:

    [DATE_FOLDER]
    # Hour when a new date-folder starts (1–24, default: 10)
    start_hour = 10
    # Minute when a new date-folder starts (00–59, default: 00)
    start_minute = 00

Adjust these values in PiBooth’s Settings menu (ESC → Settings) at any time.
Changes take effect at the start of the next photo session.

Usage
-----
1. **Snapshot original bases**  
   On configure, the plugin reads your existing quoted
   `directory` setting under `[GENERAL]` (one or more paths) and caches them.

2. **Per-session logic** (`state_wait_enter`)  
   - Builds a “threshold” datetime from `start_hour:start_minute`.  
   - If you have **changed** the threshold since the last session, it treats the next folder as **today**.  
   - Otherwise, if the current time is **before** the threshold, it treats it as **yesterday**, else **today**.  
   - Creates a subfolder named:

     YYYY-MM-DD_start-hour_HH-MM

     under each of your original base directories.  
   - Overrides PiBooth’s in-memory `directory` to the quoted list of these new folders, so that PiBooth writes into **all** of them.

No on-disk config writes are performed—the plugin never alters your config file.

Testing the Threshold
---------------------
To simulate a day-boundary without waiting 24 hours:

1. In the PiBooth Settings menu, set `start_hour`/`start_minute` to a time a few minutes **ahead** of now (for example, it’s 13:58; set to 14:00).  
2. Close the menu and take a photo session. Because this is the **first** session after changing the threshold, the plugin always treats it as **today**, so you will see a folder named with today’s date.  
3. Take one more session **before** the threshold time; now that the threshold hasn’t changed, the plugin applies “before threshold → yesterday,” creating a folder for the **previous** date.  
4. Take another session **after** the threshold time; it will create a folder for **today** again.

This way you can verify both “yesterday” and “today” folder behavior within minutes.

Examples
--------
Given in your config:

    [GENERAL]
    directory = "~/Pictures/pibooth", "~/Pictures/backup_booth"

- **Before** threshold (e.g. 10:00, time is 09:30):  
  Photos saved in  
  `"~/Pictures/pibooth/2025-07-11_start-hour_10-00", "~/Pictures/backup_booth/2025-07-11_start-hour_10-00"`

- **After** threshold (time >10:00):  
  Photos saved in  
  `"~/Pictures/pibooth/2025-07-12_start-hour_10-00", "~/Pictures/backup_booth/2025-07-12_start-hour_10-00"`

Changelog v1.3.0
----------------
- In-memory override of `GENERAL/directory` (no disk writes)  
- Preserves multiple quoted base paths and `~` prefix  
- One date-folder per threshold change or day-boundary

License
-------
MIT License

.. _pibooth: https://github.com/pibooth/pibooth
