# import time


hour = int(time.strftime('%H'))


all_my_speakers =       { 0: None,   1: None,   2: None,   3: None,   4: None,   5: None,   6: None,   7: None,   8: None,   9: None,  10: None,  11: None,
                         12: None,  13: None,  14: None,  15: None,  16: None,  17: None,  18: None,  19: None,  20: None,  21: None,  22: None,  23: None}

bedroom_mini =          { 0: 0.4,    1: 0.4,    2: 0.4,    3: 0.4,    4: 0.4,    5: 0.4,    6: 0.4,    7: 0.4,    8: 0.4,    9: 0.4,   10: 0.4,   11: 0.4,
                         12: 0.4,   13: 0.4,   14: 0.4,   15: 0.4,   16: 0.4,   17: 0.4,   18: 0.4,   19: 0.4,   20: 0.4,   21: 0.4,   22: 0.4,   23: 0.4}

bedroom_speakers =      { 0: 0.3,    1: 0.3,    2: 0.3,    3: 0.3,    4: 0.3,    5: 0.3,    6: 0.3,    7: 0.3,    8: 0.6,    9: 0.6,   10: 0.6,   11: 0.6,
                         12: 0.6,   13: 0.6,   14: 0.6,   15: 0.6,   16: 0.6,   17: 0.6,   18: 0.6,   19: 0.6,   20: 0.6,   21: 0.6,   22: 0.3,   23: 0.3}

computer_speakers =     { 0: 0.3,    1: 0.3,    2: 0.3,    3: 0.3,    4: 0.3,    5: 0.3,    6: 0.3,    7: 0.3,    8: 0.6,    9: 0.6,   10: 0.6,   11: 0.6,
                         12: 0.6,   13: 0.6,   14: 0.6,   15: 0.6,   16: 0.6,   17: 0.6,   18: 0.6,   19: 0.6,   20: 0.6,   21: 0.6,   22: 0.3,   23: 0.3}

kitchen_speakers =      { 0: None,   1: None,   2: None,   3: None,   4: None,   5: None,   6: None,   7: None,   8: None,   9: None,  10: None,  11: None,
                         12: None,  13: None,  14: None,  15: None,  16: None,  17: None,  18: None,  19: None,  20: None,  21: None,  22: None,  23: None}

kitchen_home =          { 0: 0.6,    1: 0.6,    2: 0.6,    3: 0.6,    4: 0.6,    5: 0.6,    6: 0.6,    7: 0.6,    8: 0.6,    9: 0.6,   10: 0.6,   11: 0.6,
                         12: 0.6,   13: 0.6,   14: 0.6,   15: 0.6,   16: 0.6,   17: 0.6,   18: 0.6,   19: 0.6,   20: 0.6,   21: 0.6,   22: 0.6,   23: 0.6}

living_room_speakers =  { 0: 0.3,    1: 0.3,    2: 0.3,    3: 0.3,    4: 0.3,    5: 0.3,    6: 0.3,    7: 0.3,    8: 0.6,    9: 0.6,   10: 0.6,   11: 0.6,
                         12: 0.6,   13: 0.6,   14: 0.6,   15: 0.6,   16: 0.6,   17: 0.6,   18: 0.6,   19: 0.6,   20: 0.6,   21: 0.6,   22: 0.3,   23: 0.3}


volumes = {'all_my_speakers':       (all_my_speakers, []),
           'bedroom_mini':          (bedroom_mini, []),
           'bedroom_speakers':      (bedroom_speakers, ['all_my_speakers']),
           'computer_speakers':     (computer_speakers, ['all_my_speakers', 'kitchen_speakers']),
           'kitchen_home':          (kitchen_home, ['all_my_speakers', 'kitchen_speakers']),
           'kitchen_speakers':      (kitchen_speakers, []),
           'living_room_speakers':  (living_room_speakers, ['all_my_speakers'])}


if data.get('entity_id') is not None:
    cast_name = data.get('entity_id').replace('media_player.', '')
    
    if cast_name == 'all_my_speakers':        
        cast_names = ['bedroom_speakers', 'computer_speakers', 'kitchen_home', 'living_room_speakers']
    elif cast_name == 'kitchen_speakers':
        cast_names = ['computer_speakers', 'kitchen_home']
    else:
        cast_names = [cast_name]

else:
    cast_names = ['bedroom_mini', 'bedroom_speakers', 'computer_speakers', 'kitchen_home', 'living_room_speakers']


for cast_name in cast_names:
    entity_id = 'media_player.' + cast_name
    
    # get the dictionary of volumes, determined by the hour of the day
    volume_dict = volumes.get(cast_name)[0]
    if volume_dict is not None:
        volume = volume_dict.get(hour)
        if volume is not None:
            # make sure the Chromecast is not currently playing
            state = hass.states.get(entity_id).state
            if state in ['off', 'idle']:
                set_volume = True
                
                # make sure that no groups containing the Chromecast are currently playing
                for parent_entity_id in volumes.get(cast_name)[1]:
                    if hass.states.get('media_player.' + parent_entity_id).state not in ['off', 'idle', 'unavailable']:
                        set_volume = False
                        
                # set the Chromecast's volume and volume slider
                if set_volume:
                    hass.services.call('media_player', 'volume_set', {'entity_id': entity_id, 'volume_level': volume})
                    hass.services.call('input_number', 'set_value', {'entity_id': 'input_number.' + cast_name, 'value': int(100 * volume)})

