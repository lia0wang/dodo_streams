# Assumptions
## Auth

### auth_register_v1

1. Multiple users can register with the same first names, last names and passwords.

## Channels

### channels_create_v1

1. Every channel has its unique id.
2. Channels can have the same name with different id
4. The user who created a channel becomes the owner.
5. The channel_id should be positve integers.
6. The channel is public(is_public = True) by default.

### channel_messsages_v1

1. In iteration 1, total messages is zero as messages cannot be created.
2. End return -1, in iteration 1 as there is no messages.
3. In iteraton 1, messages returns an empty list as no messages can be created.

## Channel

### channel_join_v1

1. Users can not join the channel where he/she/sth is already a member.
2. Users can join 0, 1 or more channels.

## Data store

1. There will be an entry for storing the information of users.
2. There will be an entry for storing the information of channels.
3. There will be an entry for storing messages.

## Other

1. clear_v1 will clean all the users, channels, and messages.
