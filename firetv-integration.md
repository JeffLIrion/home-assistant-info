I've got 2 Fire TV sticks that I can control via Home Assistant, both of which require authentication for ADB connections.  Here's how I got them setup and integrated into Home Assistant.

1. Download [platform-tools](https://developer.android.com/studio/releases/platform-tools.html) and connect to the first Fire TV stick from my laptop, following the instructions in this guide: [Connecting to Fire TV Through adb](https://developer.amazon.com/zh/docs/fire-tv/connecting-adb-to-device.html).

   **Important!**  You must check the box that says "always allow connections from this device." ADB authentication in Home Assistant will only work using a trusted key.

2. Connect to the second Fire TV device, following the same steps as before.  It should utilize the same ADB key.
3. Copy the `adbkey` and `adbkey.pub` files from my computer (in the folder `~/.android`) to my Home Assistant configuration folder.
4. Copy [firetv.py](https://github.com/JeffLIrion/homeassistant_native_firetv/blob/master/media_player/firetv.py) to the `custom_components/media_player/` folder in my Home Assistant configuration directory.
5. Add the Fire TV sticks to my Home Assistant configuration as follows:

   ```yaml
   media_player:
   - platform: firetv
     name: Fire TV 1
     host: 192.168.0.111
     adbkey: "/config/android/adbkey"

   - platform: firetv
     name: Fire TV 2
     host: 192.168.0.222
     adbkey: "/config/android/adbkey"

   # if your Fire TV doesn't require authentication, you would set it up like this
   - platform: firetv
     name: Fire TV 3
     host: 192.168.0.123
   ```

That's it!  No addons to worry about, and no need for automations to restart the addon when it crashes.
