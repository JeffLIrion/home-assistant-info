I've got 2 Fire TV sticks that I can control via Home Assistant.  Here's how I got them setup and stable in Hass.io.  

I used gollo's firetv-server addon from here: [http://github.com/gollo/hassio-addons](http://github.com/gollo/hassio-addons).  My addon configuration looks like this:

```json
{
  "devices": [
    {
      "name": "bedroom",
      "host": "x.x.x.x",
      "port": 5555
    },
    {
      "name": "livingroom",
      "host": "x.x.x.x",
      "port": 5555
    }
  ]
}
```

My Home Assistant configuration looks like:

```yaml
media_player:
- platform: firetv
  host: 0.0.0.0
  port: 5556
  device: bedroom
  name: Fire TV (Bedroom)

- platform: firetv
  host: 0.0.0.0
  port: 5556
  device: livingroom
  name: Fire TV (Living Room)
```

The problem is that the Fire TV server will occasionally crash.  To fix this, I created an automation that will restart the addon when the server crashes.  First, I defined a sensor to track error messages from the addon, like this:

```yaml
- platform: command_line
  name: firetv
  command: "grep -o 'Update for media_player\\.fire_tv_.*room fails' /config/home-assistant.log | wc -l"
```

Next, I created an automation that is triggered when this sensor's value changes.  Since the addon has a hyphen in its name, using `hassio.addon_restart` doesn't work, so I had to define a rest command instead:

```yaml
rest_command:
  firetv_server_restart:
    url: http://hassio/addons/d63e7be5_firetv-server/restart
    method: 'post'
```

With this in place, I defined the automation as follows:

```yaml
- id: firetv_server_restart
  alias: FireTV Server Restart
  trigger:
  - platform: state
    entity_id: sensor.firetv
  action:
  - service: rest_command.firetv_server_restart
  - service: automation.turn_off
    entity_id: automation.firetv_server_restart
  - delay: '00:05:00'
  - service: automation.turn_on
    entity_id: automation.firetv_server_restart
```

And that's it!  The two Fire TV sticks are successfully integrated into Home Assistant, and the server will restart whenever it crashes.  
