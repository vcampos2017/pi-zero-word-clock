# Raspberry Pi Zero 2 W — Waveshare 2.7-inch e-Paper Word Clock

A Python word clock for the **Raspberry Pi Zero 2 W** and **Waveshare 2.7-inch (264×176) black-and-white e-Paper HAT**.

## Clock modes

- `word_clock_epd_2in7_matrix.py`: 10×11 letter-grid word clock with highlighted words. Updates when the rounded five-minute phrase changes.
- `simple_text_clock_2in7.py`: white-background clock showing digital time and a written sentence. Updates each minute.

The matrix layout deliberately omits a separate “MINUTES” word; it says e.g. “IT IS TEN PAST EIGHT.”

## Installation

Install Raspberry Pi OS and enable SPI. Obtain the official Waveshare `e-Paper` Python examples and driver from Waveshare. These scripts expect the driver import `lib.waveshare_epd`, so copy the scripts into:

```text
/home/pi/e-Paper/RaspberryPi_JetsonNano/python/
```

Install Pillow and the DejaVu fonts if missing. Run **only one** clock process at a time:

```bash
cd ~/e-Paper/RaspberryPi_JetsonNano/python
python3 word_clock_epd_2in7_matrix.py
```

For the alternate display:

```bash
python3 simple_text_clock_2in7.py
```

## Automatic startup

Copy `wordclock.service` to `/etc/systemd/system/wordclock.service`. Its default `ExecStart` runs the matrix clock. Change that filename to `simple_text_clock_2in7.py` if desired.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now wordclock.service
systemctl status wordclock.service --no-pager
journalctl -u wordclock.service -n 50 --no-pager
```

**Important:** Stop any manually launched clock before starting the service; two processes competing for GPIO may cause `GPIO busy`. The service deliberately does **not** use an `ExecStartPre=pkill` line.

## Notes

E-paper retains its last image even if the program stops. The scripts use full refreshes, which may cause flashing and panel wear with frequent updates; check your panel's refresh recommendations before leaving the minute-by-minute mode running indefinitely. The scripts have not yet been validated on this specific device after repository preparation.

The Waveshare driver is an external dependency and is not copied into this repository.
