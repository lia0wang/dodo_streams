# Assumptions
## Auth

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

## Channel

### channel_join_v1

1. Users can not join the channel where he/she/sth is already a member.
2. Users can join 0, 1 or more channels.

## Data store

