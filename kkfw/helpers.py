
def verbSplit(text):
    if len(text.split(' ', 1)) == 1:
        verb = text.split(' ', 1)[0]
        rest_of_message = ''
    else:
        [verb, rest_of_message] = text.split(' ', 1)
    verb = verb.upper()
    return (verb, rest_of_message)
