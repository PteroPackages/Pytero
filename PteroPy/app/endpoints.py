USERS_MAIN = '/api/application/users'

def USERS_GET(u: str):
    return USERS_MAIN + u

def USERS_EXT(u: str):
    return USERS_MAIN +'/external/'+ u

NODES_MAIN = '/api/application/nodes'

def NODES_GET(n: str):
    return NODES_MAIN + n

def NODES_CONFIG(n: str):
    return NODES_MAIN + n +'/configuration'

SERVERS_MAIN = '/api/application/servers'

def SERVERS_GET(s: str):
    return SERVERS_MAIN + s

def SERVERS_EXT(s: str):
    return SERVERS_MAIN +'/external/'+ s

def SERVERS_DETAILS(s: str):
    return SERVERS_MAIN + s +'/details'

def SERVERS_BUILD(s: str):
    return SERVERS_MAIN + s +'/build'

def SERVERS_STARTUP(s: str):
    return SERVERS_MAIN + s +'/startup'

def SERVERS_SUSPEND(s: str):
    return SERVERS_MAIN + s +'/suspend'

def SERVERS_UNSUSPEND(s: str):
    return SERVERS_MAIN + s +'/unsuspend'

def SERVERS_REINSTALL(s: str):
    return SERVERS_MAIN + s +'/reinstall'

LOCATIONS = '/api/application/locations'

def LOCATIONS_GET(l: str):
    return LOCATIONS + l
