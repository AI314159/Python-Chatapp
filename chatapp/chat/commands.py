from channels.db import database_sync_to_async
from .models import Server, Message
from django.contrib.auth.models import User

# Privilege levels. This way, we can do
# if privilege >= ADMIN, ot whatever
MEMBER = 0
MODERATOR = 1
ADMIN = 2
OWNER = 3


def get_privilege(user, server):
    if server.owner == user:
        return OWNER
    elif user in server.admins.all():
        return ADMIN
    elif user in server.moderators.all():
        return MODERATOR
    else:
        return MEMBER

def set_privilege(user, server, new):
    if get_privilege(user, server) == OWNER:
        # We cannot change the privilege of the owner
        # unless we are swapping with another user, which
        # is handled elsewhere.
        return

    if new == OWNER:
        server.owner = user
        server.admins.remove(user)
        server.moderators.remove(user)

    elif new == ADMIN:
        server.admins.add(user)
        server.moderators.remove(user)
    
    elif new == MODERATOR:
        server.admins.remove(user)
        server.moderators.add(user)
    
    elif new == MEMBER:
        server.admins.remove(user)
        server.moderators.remove(user)

    server.save()

def transown(executer, server, args):
    new_owner = User.objects.get(username=args[1])
    set_privilege(new_owner, server, OWNER)


def promote(executer, server, args):
    user_to_promote = User.objects.get(username=args[1])
    executer_privilege = get_privilege(executer, server)
    promotee_privilege = get_privilege(user_to_promote, server)
    if executer_privilege >= promotee_privilege \
            and promotee_privilege + 1 < OWNER:
        set_privilege(user_to_promote, server, promotee_privilege + 1)

def demote(executer, server, args):
    user_to_demote = User.objects.get(username=args[1])
    executer_privilege = get_privilege(executer, server)
    demotee_privilege = get_privilege(user_to_demote, server)
    if executer_privilege > demotee_privilege \
            and demotee_privilege - 1 >= MEMBER \
            and demotee_privilege < OWNER:
        set_privilege(user_to_demote, server, demotee_privilege - 1)

def admin(executer, server, args):
    new_admin = User.objects.get(username=args[1])
    executer_privilege = get_privilege(executer, server)
    if executer_privilege > ADMIN:
        set_privilege(new_admin, server, ADMIN)

def mod(executer, server, args):
    new_moderator = User.objects.get(username=args[1])
    if get_privilege(new_moderator, server) != OWNER:
        set_privilege(new_moderator, server, MODERATOR)

commands = {
    # Transfer ownership to a user
    # /transown USERNAME
    "transown": {
        "n_args": 2, # Includes the command
        "fn": transown,
        "privilege": OWNER,
    },

    # Promote a user. Only works up to your own
    # level (a moderator cannot promote another
    # moderator to an admin)
    "promote": {
        "n_args": 2,
        "fn": promote,
        "privilege": MODERATOR,
    },
    
    # Demote a user. For safety, you can only
    # demote someone of a lower rank, so you need
    # to be owner or admin.
    "demote": {
        "n_args": 2,
        "fn": demote,
        "privilege": ADMIN,
    },

    # Set a user's rank to administrator
    "admin": {
        "n_args": 2,
        "fn": admin,
        "privilege": ADMIN,
    },

    # Set a user's rank to moderator
    # I don't think moderators should be able to make more moderators,
    # So the RPL is admin.
    "mod": {
        "n_args": 2,
        "fn": mod,
        "privilege": ADMIN,
    }
}

def invoke_command(server_id, username, args):
    if args[0] in commands.keys():
        executer = User.objects.get(username=username)
        server = Server.objects.get(id=server_id)
        if get_privilege(executer, server) >= commands[args[0]]["privilege"]:
            commands[args[0]]["fn"](executer, server, args)

@database_sync_to_async
def interpret_cmd(msg, username, server_id):
    if msg.startswith("/"):
        args = msg[1:].split()
        invoke_command(server_id, username, args)