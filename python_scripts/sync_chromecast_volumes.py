entity_id = data.get('entity_id')
new_volume = data.get('new_volume')

if new_volume is not None:
    new_volume = new_volume * 100.


if entity_id == 'media_player.all_my_speakers':
    entity_ids = ['media_player.kitchen_home', 'media_player.bedroom_speakers', 'media_player.computer_speakers', 'media_player.living_room_speakers']

    if new_volume is None:
        new_volume = int((float(hass.states.get('input_number.bedroom_speakers').state) + float(hass.states.get('input_number.computer_speakers').state) + float(hass.states.get('input_number.living_room_speakers').state)) * 0.33333334)

    #hass.services.call('input_number', 'set_value', {'entity_id': 'input_number.all_my_speakers', 'value': new_volume})

elif entity_id == 'media_player.kitchen_speakers':
    entity_ids = ['media_player.kitchen_home', 'media_player.computer_speakers']
    
    if new_volume is None:
        new_volume = int(float(hass.states.get('input_number.computer_speakers').state))

    #hass.services.call('input_number', 'set_value', {'entity_id': 'input_number.kitchen_speakers', 'value': new_volume})


if entity_id in ['media_player.all_my_speakers', 'media_player.kitchen_speakers']:
    # set the volumes
    for eid in entity_ids:
        hass.services.call('media_player', 'volume_set', {'entity_id': eid, 'volume_level': new_volume / 100.})

    # set the `input_number`s
    for eid in entity_ids:
        hass.services.call('input_number', 'set_value', {'entity_id': 'input_number' + eid[12:], 'value': new_volume})
