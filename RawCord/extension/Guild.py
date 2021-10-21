from .Functionals import *

from .Emoji import *
from .Guild import *
from .Channel import *

class Guild:
    def __init__(self, **kwargs):
        self.client_header = kwargs["__client__"]

        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.icon = kwargs['icon']
        self.icon_hash = Okwargs['icon_hash']
        self.splash = kwargs['splash']
        self.discovery_splash = kwargs['discovery_splash']
        self.owner = Okwargs['owner']
        self.owner_id = kwargs['owner_id']
        self.permissions = Okwargs['permissions']
        # self.region = Okwargs['region']  # NOTE: Deprecated
        self.afk_channel_id = kwargs['afk_channel_id']
        self.afk_timeout = kwargs['afk_timeout']
        self.widget_enabled = Okwargs['widget_enabled']
        self.widget_channel_id = Okwargs['widget_channel_id']
        self.verification_level = kwargs['verification_level']
        self.default_message_notifications = kwargs['default_message_notifications']
        self.explicit_content_filter = kwargs['explicit_content_filter']
        self.roles = Obrray(kwargs['roles'],None)        # NOTE: Update When Roles Created
        self.emojis = Obrray(kwargs['emojis'],Emoji)
        self.features = kwargs['features']
        self.mfa_level = kwargs['mfa_level']
        self.application_id = kwargs['application_id']
        self.system_channel_id = kwargs['system_channel_id']
        self.system_channel_flags = kwargs['system_channel_flags']
        self.rules_channel_id = kwargs['rules_channel_id']
        self.joined_at = Okwargs['joined_at']
        self.large = Okwargs['large']
        self.unavailable = Okwargs['unavailable']
        self.member_count = Okwargs['member_count']
        self.voice_states = Obrray(Okwargs['voice_states'],None)# TODO:Voice State Object
        self.members = Obrray(Okwargs['members'],Guild_Member)
        self.channels = Obrray(Okwargs['channels'],Channel,True)
        self.threads = Obrray(Okwargs['threads'],Channel,True)
        self.presences = Obrray(Okwargs['presences'],None)      # TODO: Presences Object
        self.max_presences = Okwargs['max_presences']
        self.max_members = Okwargs['max_members']
        self.vanity_url_code = kwargs['vanity_url_code']
        self.description = kwargs['description']
        self.banner = kwargs['banner']
        self.premium_tier = kwargs['premium_tier']
        self.premium_subscription_count = Okwargs['premium_subscription_count']
        self.preferred_locale = kwargs['preferred_locale']
        self.public_updates_channel_id = kwargs['public_updates_channel_id']
        self.max_video_channel_users = Okwargs['max_video_channel_users']
        self.approximate_member_count = Okwargs['approximate_member_count']
        self.approximate_presence_count = Okwargs['approximate_presence_count']
        self.welcome_screen = Okwargs['welcome_screen']# TODO:Welcom Screen Objtec
        self.nsfw_level = kwargs['nsfw_level']
        self.stage_instances = Obrray(Okwargs['stage_instances'],None)# TODO:
        self.stickers = Obrray(Okwargs['stickers'],None)# TODO:

        default_message_notifications_levels = {0:"ALL_MESSAGES",1:"ONLY_MENTIONS"}
        self.default_message_notifications_more = default_message_notifications_levels[self.default_message_notifications]
        explicit_content_filter_levels = {0:"DISABLED",1:"MEMBERS_WITHOUT_ROLES",2:"ALL_MEMBERS"}
        self.explicit_content_filter_more = explicit_content_filter_levels[self.explicit_content_filter]
        mfa_levels = {0:"NONE",1:"ELEVATED"}
        self.mfa_level_more = mfa_levels[self.mfa_level]
        verification_levels = {0:"NONE",1:"LOW",2:"MEDIUM",3:"HIGH",4:"VERY_HIGH"}
        self.verification_level_more = verification_levels[self.verification_level]
        nsfw_levels = {0:"DEFAULT",1:"EXPLICIT",2:"SAFE",3:"AGE_RESTRICTED"}
        self.nsfw_level_more = nsfw_levels[self.nsfw_level]
        premium_tiers = {0:"NONE",1:"TIER_1",2:"TIER_2",3:"TIER_3"}
        self.premium_tier_more = premium_tiers[self.premium_tier]

class Unavailable_Guild:
    def __init__(self,id=None,unavailable=True):
        self.id = id
        self.unavailable = unavailable

class Guild_Preview:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs()
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.icon = Okwargs["icon"]
        self.splash = Okwargs["splash"]
        self.discovery_splash = Okwargs["discovery_splash"]
        self.emojis = Obrrays(Okwargs["emojis"],Emoji)
        self.features = Okwargs["features"]
        self.approximate_member_count = Okwargs["approximate_member_count"]
        self.approximate_presence_count = Okwargs["approximate_presence_count"]
        self.description = Okwargs["description"]

class Guild_Widget:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.channel = kwargs["channel"]
        self.channel_id = Okwargs["channel_id"]

class Guild_Member:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.mute = kwargs["mute"]
        self.deaf = kwargs["deaf"]
        self.roles = kwargs["roles"]
        self.joined_at = kwargs["joined_at"]
        self.user = Okwargs["user"]# TODO: User Object
        self.nick = Okwargs["nick"]
        self.avatar = Okwargs["avatar"]
        self.premium_since = Okwargs["premium_since"]
        self.pending = Okwargs["pending"]
        self.permissions = Okwargs["permissions"]

class Integration:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.type = kwargs["type"]
        self.enabled = kwargs["enabled"]
        self.syncing = Okwargs["syncing"]
        self.role_id = Okwargs["role_id"]
        self.enable_emoticons = Okwargs["enable_emoticons"]
        self.expire_behavior = Okwargs["expire_behavior"]
        self.expire_grace_period = Okwargs["expire_grace_period"]
        self.user = Okwargs["user"]# TODO: User Object
        self.account = Okwargs["account"]# TODO: Account Object
        self.synced_at = Okwargs["synced_at"]
        self.subscriber_count = Okwargs["subscriber_count"]
        self.revoked = Okwargs["revoked"]
        self.application = Integration_Application(**Okwargs["application"])
        expire_behaviours = {0:"Remove Role",1:"Kick"}
        self.expire_behavior_more = expire_behaviours[self.expire_behavior]

class Integration_Account:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]

class Integration_Application:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.icon = kwargs["icon"]
        self.description = kwargs["description"]
        self.summary = kwargs["summary"]
        self.bot = Okwargs["bot"]# TODO: User Object

class Ban:
    def __init__(self, **kwargs):
        self.reason = kwargs["reason"]
        self.user = kwargs["user"]# TODO: User Object

class Welcome_Screen:
    def __init__(self, **kwargs):
        self.description = kwargs["description"]
        self.welcome_channels = kwargs["welcome_channels"]

class Welcome_Screen_Channel:
    def __init__(self, **kwargs):
        self.channel_id = kwargs["channel_id"]
        self.description = kwargs["description"]
        self.emoji_id = kwargs["emoji_id"]
        self.emoji_name = kwargs["emoji_name"]

class Partial_Channel:
    def __init__(self, **kwargs):
        self.type = kwargs["type"]
        self.name = kwargs["name"]

class Category_Channel:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.name = kwargs["name"]
        self.type = kwargs["type"]
        self.id = kwargs["id"]
        self.parent_id = Okwargs["parent_id"]
