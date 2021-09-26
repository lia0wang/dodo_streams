'''
InputError when any of:
    channel_id does not refer to a valid channel
    the authorised user is already a member of the channel
AccessError when:
    channel_id refers to a channel that is private 
    and the authorised user is not already a channel member and is not a global owner   
'''
