def standup_start_v1():
    '''
    Creates a new channel with the given name that is either a public or private channel.
    The user who created it automatically joins the channel.
    The only channel owner is the user who created the channel.
    Arguments:
        auth_user_id (int)  - The ID of the valid user.
        name (string)       - The name of the channel.
        is_public (boolean) - The state tells if the channel is private or public.
                              True for public and False for private.
    Exceptions:
        InputError - Length of name is less than 1 or more than 20 characters.
    Return Value:
        Return a dictionary containing a valid channel_id.
    '''
