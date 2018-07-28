# Intro

I have 3 Chromecast Audio devices, plus a Google Home and a Google Home Mini.  Group playback is awesome... when all my speakers are playing at the same volume.  Unfortunately, the volume levels can get out of sync due to

1. Keeping my Google Home at a louder volume than my Chromecast Audio devices (so that I can hear what Google says).
2. Playing music on a group that includes my Google Home, then telling Google "louder" or "softer", which will change the volume of the Google Home but not the other group members.
3. Playing music on 1 or more devices and changing the volume level, then later playing music on a group which includes those devices.

So I set out to use Home Assistant to ensure that when casting to a group, all speakers remain at the same volume.


# 1. Setup

For starters, here are the Chromecast Audio devices that I include in my setup:

```yaml
media_player:
  - platform: cast
    host: !secret bedroom_mini_ip_address
    name: Bedroom Mini

#  - platform: cast
#    host:
#    name: All My Speakers

  - platform: cast
    host: !secret bedroom_speakers_ip_address
    name: Bedroom Speakers

  - platform: cast
    host: !secret computer_speakers_ip_address
     name: Computer Speakers

  - platform: cast
    host: !secret kitchen_home_ip_address
    name: Kitchen Home

#  - platform: cast
#    host:
#    name: Kitchen Speakers

  - platform: cast
    host: !secret living_room_speakers_ip_address
    name: Living Room Speakers

#  - platform: cast
#    host:
#    name: Main Speakers
```


The three devices that are commented out -- "All My Speakers," "Kitchen Speakers," and "Main Speakers" -- are cast groups that don't have an IP address, and so they must be automatically discovered by Home Assistant.  Their members are:

* All My Speakers

  * Bedroom Speakers
  * Computer Speakers
  * Kitchen Home
  * Living Room Speakers

* Kitchen Speakers

  * Computer Speakers
  * Kitchen Home

* Main Speakers

  * Computer Speakers
  * Kitchen Home
  * Living Room Speakers

It's worth mentioning that I have a Python script that I use to set the Chromecast volumes each hour, as well as an automation that calls it.  The Python script is [set_chromecast_volumes.py](./python_scripts/set_chromecast_volumes.py) and the automation is [set_chromecast_volumes_hourly.yaml](./automations/chromecast_audio/set_chromecast_volumes_hourly.yaml).  I also use that Python script to set the volume of my Google Home when group playback stops.


## 1a. Home Assistant Groups

In Home Assistant, I created a group for each Chromecast Audio group, as follows:

```yaml
all_my_speakers:
  name: All My Speakers
  icon: mdi:cast
  entities:
  - input_number.bedroom_speakers
  - input_number.computer_speakers
  - input_number.kitchen_home
  - input_number.living_room_speakers


kitchen_speakers:
  name: Kitchen Speakers
  icon: mdi:cast
  entities:
  - input_number.computer_speakers
  - input_number.kitchen_home


main_speakers:
  name: Main Speakers
  icon: mdi:cast
  entities:
  - input_number.computer_speakers
  - input_number.kitchen_home
  - input_number.living_room_speakers
```


## 1b. Input Numbers

The challenge in all of this is that Home Assistant only knows the (average) volume of the group, not the volumes of the group members.  In order to get around this, I'll need to track the volume of both the individual speakers and the Chromecast Audio groups.  To do this, I defined an `input_number` for each Chromecast, including the groups:

```yaml
input_number:
  all_my_speakers:
    name: All My Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  bedroom_mini:
    name: Bedroom Mini
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  bedroom_speakers:
    name: Bedroom Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  computer_speakers:
    name: Computer Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  kitchen_home:
    name: Kitchen Home
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  kitchen_speakers:
    name: Kitchen Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  living_room_speakers:
    name: Living Room Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1

  main_speakers:
    name: Main Speakers
    icon: mdi:sort-numeric
    min: 0
    max: 100
    step: 1
```


## 1c. Sensors

I also defined sensors to display these volumes, with the icon indicating whether the device is currently playing.  Note that for the groups, the value of the sensor is the average of its members, excluding the Google Home.  

```yaml
- platform: template
  sensors:
    all_my_speakers:
      friendly_name: "All My Speakers"
      entity_id:
      - media_player.all_my_speakers
      - input_number.all_my_speakers
      - input_number.bedroom_speakers
      - input_number.computer_speakers
      - input_number.living_room_speakers
      value_template: >
          {% if is_state('media_player.all_my_speakers', 'off') %}
              {{ ( float(states('input_number.bedroom_speakers')) + float(states('input_number.computer_speakers')) + float(states('input_number.living_room_speakers')) ) | multiply(0.33333334) | round(0) }}
          {% else %}
              {{ states('input_number.all_my_speakers') | round(0) }}
          {% endif %}
      icon_template: "{% if is_state('media_player.all_my_speakers', 'off') or is_state('media_player.all_my_speakers', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    bedroom_mini:
      friendly_name: "Bedroom Mini"
      entity_id:
      - input_number.bedroom_mini
      - media_player.bedroom_mini
      value_template: "{{ states('input_number.bedroom_mini') | round(0) }}"
      icon_template: "{% if is_state('media_player.bedroom_mini', 'off') or is_state('media_player.bedroom_mini', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    bedroom_speakers:
      friendly_name: "Bedroom Speakers"
      entity_id:
      - input_number.bedroom_speakers
      - media_player.bedroom_speakers
      value_template: "{{ states('input_number.bedroom_speakers') | round(0) }}"
      icon_template: "{% if is_state('media_player.bedroom_speakers', 'off') or is_state('media_player.bedroom_speakers', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    computer_speakers:
      friendly_name: "Computer Speakers"
      entity_id:
      - input_number.computer_speakers
      - media_player.computer_speakers
      value_template: "{{ states('input_number.computer_speakers') | round(0) }}"
      icon_template: "{% if is_state('media_player.computer_speakers', 'off') or is_state('media_player.computer_speakers', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    kitchen_home:
      friendly_name: "Kitchen Home"
      entity_id:
      - input_number.kitchen_home
      - media_player.kitchen_home
      value_template: "{{ states('input_number.kitchen_home') | round(0) }}"
      icon_template: "{% if is_state('media_player.kitchen_home', 'off') or is_state('media_player.kitchen_home', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    kitchen_speakers:
      friendly_name: "Kitchen Speakers"
      entity_id:
      - media_player.kitchen_speakers
      - input_number.kitchen_speakers
      - input_number.computer_speakers
      value_template: >
          {% if is_state('media_player.kitchen_speakers', 'off') %}
              {{ states('input_number.computer_speakers') | round(0) }}
          {% else %}
              {{ states('input_number.kitchen_speakers') | round(0) }}
          {% endif %}
      icon_template: "{% if is_state('media_player.kitchen_speakers', 'off') or is_state('media_player.kitchen_speakers', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"

    main_speakers:
      friendly_name: "Main Speakers"
      entity_id:
      - media_player.main_speakers
      - input_number.computer_speakers
      - input_number.living_room_speakers
      - input_number.main_speakers
      value_template: >
          {% if is_state('media_player.main_speakers', 'off') %}
              {{ ( float(states('input_number.computer_speakers')) + float(states('input_number.living_room_speakers')) ) | multiply(0.5) | round(0) }}
          {% else %}
              {{ states('input_number.main_speakers') | round(0) }}
          {% endif %}
      icon_template: "{% if is_state('media_player.main_speakers', 'off') or is_state('media_player.main_speakers', 'unavailable') %}mdi:cast{% else %}mdi:cast-connected{% endif %}"
```


## 1d. Setup summary

Naming is important!  At this point, for every Chromecast audio group you will have the following in Home Assistant:

* `media_player.<chromecast_audio_group>`
* `group.<chromecast_audio_group>`
* `input_number.<chromecast_audio_group>`
* `sensor.<chromecast_audio_group>`


# 2. Simple automations

## 2a. Track individual volumes

Using automations to track individual volumes was pretty simple (see [individual_volumes.yaml](./automations/chromecast_audio/individual_volumes.yaml)):

```yaml
- id: track_volume_individual
  alias: "CCA: Track volume (individual)"
  trigger:
  - platform: state
    entity_id: media_player.bedroom_mini, media_player.bedroom_speakers, media_player.computer_speakers, media_player.kitchen_home, media_player.living_room_speakers
  condition:
  - condition: template
    value_template: "{{ trigger.to_state.attributes.volume_level is defined and trigger.to_state.attributes.volume_level | multiply(100) | round(0) != states('input_number.%s'|format(trigger.to_state.object_id)) }}"
  action:
  - service: input_number.set_value
    data_template:
      entity_id: "{{ 'input_number.%s'|format(trigger.to_state.object_id) }}"
      value: "{{ trigger.to_state.attributes.volume_level | multiply(100) | round(0) }}"
```


## 2b. Synchronize volume levels when group playback starts

The next step was to create an automation that would synchronize the volume levels when group playback started.  This was simple enough (see [group_playback_start.yaml](./automations/chromecast_audio/group_playback_start.yaml):

```yaml
- id: group_playback_start
  alias: "CCA: Group playback (start)"
  trigger:
  - platform: state
    entity_id: media_player.all_my_speakers, media_player.kitchen_speakers, media_player.main_speakers
    from: 'off'
  condition:
  - condition: template
    value_template: "{{ trigger.to_state.state in ['idle', 'paused', 'playing'] }}"
  action:
  - service: python_script.cca_sync_chromecast_volumes
    data:
      entity_id: "{{ trigger.entity_id }}"
```


## 2c. Update the group volume trackers when a group is playing

I need an automation that will update my trackers (i.e., `input_number.<group_object_id>`) for the group volumes when they are NOT playing by averaging the volumes of their members, excluding the Kitchen Home.  Using my `sensor.all_my_speakers`, `sensor.kitchen_speakers`, and `sensor.main_speakers` template sensors, defined above, this is pretty easy (see [group_volumes.yaml](./automations/chromecast_audio/group_volumes.yaml):

```yaml
- id: track_volume_group_off
  alias: "CCA: Track volume (group [off])"
  trigger:
  - platform: state
    entity_id: sensor.all_my_speakers, sensor.kitchen_speakers, sensor.main_speakers
  condition:
  - condition: template
    value_template: "{{ states('media_player.%s'|format(trigger.to_state.object_id)) in ['off', 'unavailable'] }}"
  action:
  - service: input_number.set_value
    data_template:
      entity_id: "{{ 'input_number.%s'|format(trigger.to_state.object_id) }}"
      value: "{{ states('sensor.%s'|format(trigger.to_state.object_id)) }}"
```


## 2d. Restore the Google Home volume when group playback stops

I also need an automation to set my Google Home volume back to baseline when playback stops.  For this, I utilized my [set_chromecast_volumes.py](./python_scripts/set_chromecast_volumes.py) Python script once again.  The automation is (see [group_playback_stop.yaml](./automations/chromecast_audio/group_playback_stop.yaml):

```yaml
- id: group_playback_stop
  alias: "CCA: Group playback (stop)"
  trigger:
  - platform: state
    entity_id: media_player.all_my_speakers, media_player.kitchen_speakers, media_player.main_speakers
    to: 'off'
  condition:
  - condition: template
    value_template: "{{ trigger.from_state.state in ['idle', 'paused', 'playing'] }}"
  action:
  - service: python_script.cca_set_chromecast_volumes
    data:
      entity_id: media_player.kitchen_home
```


# 3. Complicated automations

Now for the hard part!  I need to define two automations.  For both automations, the trigger is a change in the state of a Chromecast Audio group media player, and their first condition is that the media player volume is not equal to the tracker volume.  The difference is in their second condition:

* If `input_number.<group_object_id> == input_number.<member_object_id>` for all the members of the group, then the system was normalized and now the volume has been changed, and so we need to (1) update the group volume tracker, `input_number.<group_object_id>`, (2) set the volume of each group member to this new volume, and (3) set the tracker for each group member, `input_number.<member_object_id>`, to the new value, `input_number.<group_object_id>`.  See the automation `track_and_normalize_volume_group` below.
* Otherwise, the member volumes were not normalized and the (average) group volume only changed because the member volumes are being normalized.  In this case, we simply need to (1) set the volume of each group member to the value of `input_number.<group_object_id>` and (2) set the tracker for each group member, `input_number.<member_object_id>`, to `input_number.<group_object_id>`.  See the automation `normalize_volume_group` below.

Fortunately, instead of defining different automations for each group, I can use templating along with the groups and input numbers that I've defined (see [group_volumes.yaml](./automations/chromecast_audio/group_volumes.yaml)).  

```yaml
# all volumes are the same --> track and normalize
- id: track_and_normalize_volume_group
  alias: "CCA: Track and normalize volume (group)"
  trigger:
  - platform: state
    entity_id: media_player.all_my_speakers, media_player.kitchen_speakers, media_player.main_speakers
  condition:
    condition: and
    conditions:
    - condition: template
      value_template: "{{ trigger.to_state.attributes.volume_level is defined and trigger.to_state.attributes.volume_level | multiply(100) | round(0) | int != states('input_number.%s'|format(trigger.to_state.object_id)) | int }}"
    - condition: template
      value_template: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id if states(entity_id) != states('input_number.%s'|format(trigger.to_state.object_id)) -%}
        {%- if loop.first -%}false{%- endif -%}
        {%- else -%}
        true
        {%- endfor -%}
  action:
  # 1) Set group tracker
  - service: input_number.set_value
    data_template:
      entity_id: "{{ 'input_number.%s'|format(trigger.to_state.object_id) }}"
      value: "{{ trigger.to_state.attributes.volume_level | multiply(100) | round(0) | int }}"

  # 2) Set individual volumes
  - service: media_player.volume_set
    data_template:
      entity_id: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id -%}
        {{ entity_id|replace('input_number', 'media_player') }}
        {%- if not loop.last -%}, {%- endif -%}
        {%- endfor -%}
      volume_level: "{{ trigger.to_state.attributes.volume_level }}"

  # 3) Set individual trackers
  - service: input_number.set_value
    data_template:
      entity_id: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id -%}
        {{ entity_id }}
        {%- if not loop.last -%}, {%- endif -%}
        {%- endfor -%}
      value: "{{ trigger.to_state.attributes.volume_level | multiply(100) | round(0) | int }}"



# all volumes are NOT the same --> normalize only
- id: normalize_volume_group
  alias: "CCA: Normalize volume (group)"
  trigger:
  - platform: state
    entity_id: media_player.all_my_speakers, media_player.kitchen_speakers, media_player.main_speakers
  condition:
    condition: and
    conditions:
    - condition: template
      value_template: "{{ trigger.to_state.attributes.volume_level is defined and trigger.to_state.attributes.volume_level | multiply(100) | round(0) | int != states('input_number.%s'|format(trigger.to_state.object_id)) | int }}"
    - condition: template
      value_template: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id if states(entity_id) != states('input_number.%s'|format(trigger.to_state.object_id)) -%}
        {%- if loop.first -%}true{%- endif -%}
        {%- else -%}
        false
        {%- endfor -%}
  action:
  # 1) Set individual volumes
  - service: media_player.volume_set
    data_template:
      entity_id: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id -%}
        {{ entity_id|replace('input_number', 'media_player') }}
        {%- if not loop.last -%}, {%- endif -%}
        {%- endfor -%}
      volume_level: "{{ states('input_number.%s'|format(trigger.to_state.object_id)) | multiply(0.01) }}"

  # 2) Set individual trackers
  - service: input_number.set_value
    data_template:
      entity_id: >
        {%- for entity_id in states.group[trigger.to_state.object_id].attributes.entity_id -%}
        {{ entity_id }}
        {%- if not loop.last -%}, {%- endif -%}
        {%- endfor -%}
      value: "{{ states('input_number.%s'|format(trigger.to_state.object_id)) }}"
```


# Bonus

Sometimes a Chromecast Audio group will become unavailable in Home Assistant.  To deal with this case, I created an automation that will restart Home Assistant if a Chromecast group is unavailable for 2 minutes (see [group_unavailable.yaml](./automations/chromecast_audio/group_unavailable.yaml):

```yaml
- id: group_unavailable
  alias: "CCA: Group unavailable"
  trigger:
  - platform: state
    entity_id: media_player.all_my_speakers, media_player.kitchen_speakers, media_player.main_speakers
    to: 'unavailable'
    for:
      minutes: 2
  action:
  - service: homeassistant.restart
```
