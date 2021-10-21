from .Functionals import *

class Audit_Log:
    def __init__(self,webhooks,users,audit_log_entries,integrations,threads):
        self.webhooks = webhooks
        self.users = users
        self.audit_log_entries = [Audit_Log_Entry(**i) for i in audit_log_entries]
        self.integrations = integrations
        self.threads = threads
        self.help = "\nSee Audit_Log methods at [https://discord.com/developers/docs/resources/audit-log#audit-log-object-audit-log-structure]\n"

class Audit_Log_Entry:
    def __init__(self,**kwargs):
        kwargs = OptionalKwargs(kwargs)
        self.target_id = kwargs["target_id"]
        self.changes = [Audit_Log_Change(**i) for i in kwargs["changes"]]
        self.user_id = kwargs["user_id"]
        self.id = kwargs["id"]
        self.action_type = kwargs["action_type"]
        self.options = kwargs["options"]
        self.reason = kwargs["reason"]

        audit_log_events = {1: 'GUILD_UPDATE', 10: 'CHANNEL_CREATE', 11: 'CHANNEL_UPDATE', 12: 'CHANNEL_DELETE', 13: 'CHANNEL_OVERWRITE_CREATE', 14: 'CHANNEL_OVERWRITE_UPDATE', 15: 'CHANNEL_OVERWRITE_DELETE', 20: 'MEMBER_KICK', 21: 'MEMBER_PRUNE', 22: 'MEMBER_BAN_ADD', 23: 'MEMBER_BAN_REMOVE', 24: 'MEMBER_UPDATE', 25: 'MEMBER_ROLE_UPDATE', 26: 'MEMBER_MOVE', 27: 'MEMBER_DISCONNECT', 28: 'BOT_ADD', 30: 'ROLE_CREATE', 31: 'ROLE_UPDATE', 32: 'ROLE_DELETE', 40: 'INVITE_CREATE', 41: 'INVITE_UPDATE', 42: 'INVITE_DELETE', 50: 'WEBHOOK_CREATE', 51: 'WEBHOOK_UPDATE', 52: 'WEBHOOK_DELETE', 60: 'EMOJI_CREATE', 61: 'EMOJI_UPDATE', 62: 'EMOJI_DELETE', 72: 'MESSAGE_DELETE', 73: 'MESSAGE_BULK_DELETE', 74: 'MESSAGE_PIN', 75: 'MESSAGE_UNPIN', 80: 'INTEGRATION_CREATE', 81: 'INTEGRATION_UPDATE', 82: 'INTEGRATION_DELETE', 83: 'STAGE_INSTANCE_CREATE', 84: 'STAGE_INSTANCE_UPDATE', 85: 'STAGE_INSTANCE_DELETE', 90: 'STICKER_CREATE', 91: 'STICKER_UPDATE', 92: 'STICKER_DELETE', 110: 'THREAD_CREATE', 111: 'THREAD_UPDATE', 112: 'THREAD_DELETE'}
        self.action_type_more = audit_log_events[self.action_type]

        self.help = "\nSee Audit_Log_Entry properties at [https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-audit-log-entry-structure]\n"

class Audit_Log_Change:
    def __init__(self,**kwargs):
        kwargs = OptionalKwargs(kwargs)
        self.new_value = kwargs["new_value"]
        self.old_value = kwargs["old_value"]
        self.key = kwargs["key"]
        self.help = "\nSee Audit_Log_Change properties at [https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-structure]\n"
