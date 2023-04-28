'''
Define a function called url_checker that accepts the following argument:

url - a URL string
Return:

If both the protocol and the store ID are invalid:
print two lines:
'{protocol} is an invalid protocol.'
'{store_id} is an invalid store ID.'
If only the protocol is invalid:
print:
'{protocol} is an invalid protocol.'
If only the store ID is invalid:
print:
'{store_id} is an invalid store ID.'
If both the protocol and the store ID are valid, return the store ID.

'''

def url_checker(url):
    url = url.split('/')
    protocol = url[0]
    store_id = url[-1]
    if protocol != "https:" and len(store_id) != 7: 
        print("{} is an invalid protocol. \n{} is an invalid store ID".format(protocol,store_id))
    elif protocol != "https:" and len(store_id) == 7:
        print("{} is an invalid protocol.".format(protocol))
    elif protocol == "https:" and len(store_id) != 7:
        print("{} is an invalid store ID.".format(store_id))
    else:
        print(store_id)

# RUN THIS CELL TO TEST YOUR FUCTION            # Should return:
url_checker('http://exampleURL1.com/r626c3')    # 'http: is an invalid protocol.'
print()                                         # 'r626c3 is an invalid store ID.'
url_checker('ftps://exampleURL1.com/r626c36')   # 'ftps: is an invalid protocol.
print()
url_checker('https://exampleURL1.com/r626c3')   # 'r626c3 is an invalid store ID.'
print()
url_checker('https://exampleURL1.com/r626c36')  # 'r626c36'