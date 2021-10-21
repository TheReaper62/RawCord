from .Functionals import *

class Channel:
    def __init__(self,**kwargs):
        self.client_header = kwargs["__client__"]

        self.id = kwargs["id"]
        self.type = kwargs["type"]
        Okwargs = OptionalKwargs(kwargs)
        self.guild_id = Okwargs["guild_id"]
        self.position = Okwargs["position"]
        self.permission_overwrites = Okwargs["permission_overwrites"]
        self.name = Okwargs["name"]
        self.topic = Okwargs["topic"]
        self.nsfw = boolean(Okwargs["nsfw"])
        self.last_message_id = Okwargs["last_message_id"]
        self.bitrate = Okwargs["bitrate"]
        self.user_limit = Okwargs["user_limit"]
        self.rate_limit_per_user = Okwargs["rate_limit_per_user"]
        self.recipients = Okwargs["recipients"]
        self.icon = Okwargs["icon"]
        self.owner_id = Okwargs["owner_id"]
        self.application_id = Okwargs["application_id"]
        self.parent_id = Okwargs["parent_id"]
        self.last_pin_timestamp = Okwargs["last_pin_timestamp"]
        self.rtc_region = Okwargs["rtc_region"]
        self.video_quality_mode = Okwargs["video_quality_mode"]
        self.message_count = Okwargs["message_count"]
        self.member_count = Okwargs["member_count"]
        self.thread_metadata = Okwargs["thread_metadata"]
        self.member = Okwargs["member"]
        self.default_auto_archive_duration = Okwargs["default_auto_archive_duration"]
        self.permissions = Okwargs["permissions"]

        channel_types = {0: 'GUILD_TEXT', 1: 'DM', 2: 'GUILD_VOICE', 3: 'GROUP_DM', 4: 'GUILD_CATEGORY', 5: 'GUILD_NEWS', 6: 'GUILD_STORE', 10: 'GUILD_NEWS_THREAD', 11: 'GUILD_PUBLIC_THREAD', 12: 'GUILD_PRIVATE_THREAD', 13: 'GUILD_STAGE_VOICE'}
        self.type_more = OptionalKwargs(channel_types)[self.type]

        if self.video_quality_mode != None:
            voice_quality_modes = {"1":"AUTO","2":"FULL"}
            self.video_quality_mode_more = OptionalKwargs(voice_quality_modes)[self.video_quality_mode]

        self.help = "\nSee Audit_Log_Object methods at [https://discord.com/developers/docs/resources/channel#channel-object-channel-structure]\n"

    def modify(self,**kwargs):
        path = BASE + f"channels/{self.id}"

        # Captures GROUP DMs ONlY
        if "GROUP_DM" == self.type_more:
            expected_args = ["reason","name","icon"]

        # Capture Normal Guild Channels(Inc. Voice)
        elif self.type_more.startswith("GUILD") and not(self.type_more.endswith("THREAD")):
            expected_args = ["reason",'name', 'type', 'position', 'topic', 'nsfw', 'rate_limit_per_user', 'bitrate', 'user_limit', 'permission_overwrites', 'parent_id', 'rtc_region', 'video_quality_mode', 'default_auto_archive_duration']

        # Captures Threads
        elif self.type_more.endswith("THREAD"):
            expected_args = ["reason",'name', 'archived', 'auto_archive_duration', 'locked', 'invitable', 'rate_limit_per_user']
        else:
            return

        if not valid_kwargs(kwargs,expected_args):  return

        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.patch(path,headers=headers,json=kwargs)

        # if r.status_code == 429:
        #     raise RateLimit(f"{r.json['message']}\nRetry After {r.json['retry_after']} seconds")
        #     return
        return Channel(**r.json)

    def delete(self,**kwargs):
        path = BASE + f"/channels/{self.id}"

        expected_args = ["reason"]
        if not valid_kwargs(kwargs,expected_args): return

        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.delete(path,headers=headers,json=kwargs)
        debrief_request(r,self,kwargs)

    def get_messages(self,**kwargs):
        path = BASE+f"/channels/{self.id}/messages"
        keywords = ["around","before","after","limit"]
        r = requests.get(process_query(path,keywords,kwargs),headers=self.client_header)
        debrief_request(r,self,kwargs)
        arguments = r.json()
        messages = [Message(**{**i,**{"__client__":self.client_header}}) for i in arguments][::-1]
        return messages

    # A Shorthand is available through Client.get_message()
    # use this instead cos this one superior
    def get_message(self,**kwargs):
        expected_args = ["message_id"]
        if not valid_kwargs(kwargs,expected_args):  return
        path = BASE + f"/channels/{self.id}/messages/{kwargs['message_id']}"
        r = requests.get(path,headers=self.client_header)
        debrief_request(r,self,kwargs)
        return Message(**{**r.json(),**{"__client__":self.client_header}})

    def create_message(self,**kwargs):
        path = BASE + f"/channels/{self.id}/messages"
        Okwargs = OptionalKwargs(kwargs)
        if Okwargs["embeds"] != None:
            Okwargs.dictionary["embeds"] = [i.raw for i in Okwargs["embeds"]]
        r = requests.post(path,headers=self.client_header,json=Okwargs.dictionary)
        debrief_request(r,self,kwargs)
        return Message(**{**r.json(),**{"__client__":self.client_header}})

    def crosspost_message(self, **kwargs):
        expected_args = ["message_id"]
        if not valid_kwargs(kwargs,expected_args):  return
        path = BASE + f"/channels/{self.id}/messages/{kwargs['message_id']}/crosspost"
        r = requests.post(path,headers=self.client_header,json=kwargs)
        debrief_request(r,self,kwargs)
        return Message(**{**r.json(),**{"__client__":self.client_header}})
    # NOTE: Not been tested cos idk what crossposting is lol

    def edit_message(self,**kwargs):
        expected_args = ["message_id"]
        path = BASE + f"/channels/{self.id}/messages/{kwargs['message_id']}"
        Okwargs = OptionalKwargs(kwargs)
        if Okwargs["embeds"] != None:
            Okwargs.dictionary["embeds"] = [i.raw for i in Okwargs["embeds"]]
        r = requests.patch(path,headers=self.client_header,json=Okwargs.dictionary)
        debrief_request(r,self,kwargs)
        return Message(**{**r.json(),**{"__client__":self.client_header}})
        # NOTE: To be tested

    def delete_message(self, **kwargs):
        expected_args = ["message_id","reason"]
        path = BASE + f"/channels/{self.id}/messages/{kwargs['message_id']}"
        if not valid_kwargs(kwargs,expected_args): return
        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.delete(path,headers=headers,json=kwargs)
        debrief_request(r,self,kwargs)
        # NOTE: To be tested
        # NOTE: To be made a Message Object Method as well

    def bulk_delete_message(self, **kwargs):
        expected_args = ["message_ids","reason"]
        path = BASE + f"/channels/{self.id}/messages/bulk-delete"
        if not valid_kwargs(kwargs,expected_args): return
        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.post(path,headers=headers,json=kwargs)
        debrief_request(r,self,kwargs)
        # NOTE: To be tested

    def get_invites(self):
        path = BASE + f"/channels/{self.id}/invites"
        r = requests.get(path,headers=self.client_header)
        debrief_request(r,self)
        arguments = r.json()
        return arguments
        # inivtes = [Invite(**{**i,**{"__client__":self.client_header}}) for i in arguments][::-1]
        # NOTE: To be updated when Invite Object Created

    def create_invite(self, **kwargs):
        optional_kwargs = ["max_age","max_uses","temporary","unique","target_type","target_user_id","target_application_id"]
        kwargs = {i:kwargs[i] for i in kwargs if i in optional_kwargs}
        path = BASE + f"/channels/{self.id}/invites"
        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.post(path,headers=headers,json=kwargs)
        debrief_request(r,self,kwargs)
        # NOTE: To be updated when Invite Object Created
        # TODO: return Invite Object

    def delete_permission(self, **kwargs):
        expected_args = ["overwrite_id","reason"]
        path = BASE + f"/channels/{self.id}/permissions/{overwrite_id}"
        if not valid_kwargs(kwargs,expected_args): return
        kwargs,headers = add_audit_reason(kwargs,self.client_header)
        r = requests.delete(path,headers=headers,json=kwargs)
        debrief_request(r,self,kwargs)

    def follow_news_channel(self, **kwargs):
        expected_args = ["webhook_channel_id"]
        path = BASE + f"/channels/{self.id}/followers"
        if not valid_kwargs(kwargs,expected_args): return
        r = requests.post(path,headers=self.client_header,json=kwargs)
        debrief_request(r,self,kwargs)
        return Followed_Channel(**r.json())

    def trigger_typing(self):
         path = BASE + f"/channels/{self.id}/typing"
         r = requests.get(path,headers=self.client_header)
         debrief_request(r,self)

    def get_pinned(self):
        path = BASE + f"/channels/{self.id}/pins"
        r = requests.get(path,headers=self.client_header)
        debrief_request(r,self)
        messages = [Message(**{**i,**{"__client__":self.client_header}}) for i in r.json()][::-1]
        return messages

    def group_dm_add(self, **kwargs):
        expected_args = ["access_token","nick", "user_id"]
        if not valid_kwargs(kwargs,expected_args):  return
        path = BASE + f"/channels/{self.id}/recipients/{kwargs['user_id']}"
        r = request.put(path, headers=self.client_header, json=kwargs)
        debrief_request(r,self,kwargs)

    def group_dm_remove(self, **kwargs):
        expected_args = ["user_id"]
        if not valid_kwargs(kwargs,expected_args): return
        path = BASE + f"/channels/{channel.id}/recipients/{kwargs['user_id']}"
        r = request.delete(path, headres=self.client_header)
        debrief_request(r,self)

    def start_thread(self, **kwargs):
        expected_args = ["name","auto_archive_duration", "type", "invitable","reason"]
        if not str(type).isdigit():
            if str(type).upper() not in CHANNEL_TYPES:
                raise InvalidArguments("Make sure type is a valid Number or make sure the name is spelt correctly.\nExample: 'GUILD_TEXT'")
                return
            type = CHANNEL_TYPES[type.upper()]
        if not valid_kwargs(kwargs,expected_args):  return
        path = BASE + f"/channels/{self,channel_id}/messages/{self.id}/threads"
        kwargs, headers = add_audit_reason(kwargs, self.client_header)
        r = request.post(path, headers=headers,json=kwargs)
        debrief_request(r,self)
        return Channel(**{**r.json(),**{"__client__":self.client_header}})

class Message:
        def __init__(self,**kwargs):
            self.client_header = kwargs["__client__"]

            Okwargs = OptionalKwargs(kwargs)
            self.id = kwargs["id"]
            self.channel_id = kwargs["channel_id"]
            self.author = kwargs["author"]
            self.content = kwargs["content"]
            self.timestamp = kwargs["timestamp"]
            self.edited_timestamp = kwargs["edited_timestamp"]
            self.tts = boolean(kwargs["tts"])
            self.mention_everyone = boolean(kwargs["mention_everyone"])
            self.mentions = kwargs["mentions"]
            self.mention_roles = kwargs["mention_roles"]
            self.attachments = kwargs["attachments"]
            self.embeds = kwargs["embeds"]
            self.pinned = boolean(kwargs["pinned"])
            self.type = kwargs["type"]

            self.guild_id = Okwargs["guild_id"]
            self.member = Okwargs["member"]
            self.mention_channels = Okwargs["mention_channels"]
            self.reactions = Okwargs["reactions"]
            self.nonce = Okwargs["nonce"]
            self.webhook_id = Okwargs["webhook_id"]
            self.activity = Okwargs["activity"]
            self.application = Okwargs["application"]
            self.application_id = Okwargs["application_id"]
            self.message_reference = Okwargs["message_reference"]
            self.flags = Okwargs["flags"]
            self.referenced_message = Okwargs["referenced_message"]
            self.interaction = Okwargs["interaction"]
            self.thread = Okwargs["thread"]
            self.components = Okwargs["components"] # NOTE: Change to Message components Obect once Created
            self.sticker_items = Okwargs["sticker_items"]
            self.stickers = Okwargs["stickers"]

            message_types = ['DEFAULT', 'RECIPIENT_ADD', 'RECIPIENT_REMOVE', 'CALL', 'CHANNEL_NAME_CHANGE', 'CHANNEL_ICON_CHANGE', 'CHANNEL_PINNED_MESSAGE', 'GUILD_MEMBER_JOIN', 'USER_PREMIUM_GUILD_SUBSCRIPTION', 'USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1', 'USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2', 'USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3', 'CHANNEL_FOLLOW_ADD', 'GUILD_DISCOVERY_DISQUALIFIED', 'GUILD_DISCOVERY_REQUALIFIED', 'GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING', 'GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING', 'THREAD_CREATED', 'REPLY', 'CHAT_INPUT_COMMAND', 'THREAD_STARTER_MESSAGE', 'GUILD_INVITE_REMINDER', 'CONTEXT_MENU_COMMAND']
            self.type_more = message_types[self.type]

        def react(self, **kwargs):
            expected_args = ["emoji"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions/{kwargs['emoji']}/@me"
            r = requests.put(path,headers=self.client_header)
            debrief_request(r,self,kwargs)

        def unreact(self, **kwargs):
            expected_args = ["emoji"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions/{kwargs['emoji']}/@me"
            r = requests.delete(path,headers=self.client_header)
            debrief_request(r,self,kwargs)

        def remove_user_reaction(self, **kwargs):
            expected_args = ["emoji", "user_id"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions/{kwargs['emoji']}/{kwargs['user_id']}"
            r = requests.delete(path,headers=self.client_header)
            debrief_request(r,self,kwargs)
        # Alias
        remove_reaction = remove_user_reaction

        def get_reactions(self, **kwargs):
            expected_args = ["emoji"]
            keywords = ["after","limit"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions/{kwargs['emoji']}"
            r = requests.get(process_query(path,keywords,kwargs),headers=self.client_header)
            debrief_request(r,self,kwargs)
            arguments = r.json
            return arguments
            # NOTE: Update when User Object created
            # NOTE: Create Client Method
            # users = [User(**i) for i in arguments][::-1]
            # return users

        def remove_all_reactions(self):
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions"
            r = requests.delete(path,headers=self.client_header)
            debrief_request(r,self)
        # Alias
        clear_reactions = remove_all_reactions

        def react(self, **kwargs):
            expected_args = ["emoji"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
            r = requests.put(path,headers=self.client_header)
            debrief_request(r,self,kwargs)

        def pin_message(self, **kwargs):
            expected_args = ["reason"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/pins/{self.id}"
            kwargs, headers = add_audit_reason(kwargs, self.client_header)
            r = requests.put(path,headers=headers)
            debrief_request(r,self)
        # Alias
        pin = pin_message

        def unpin_message(self, **kwargs):
            expected_args = ["reason"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self.channel_id}/pins/{self.id}"
            kwargs, headers = add_audit_reason(kwargs, self.client_header)
            r = requests.delete(path,headers=headers)
            debrief_request(r,self)
        # Alias
        unpin = unpin_message

        def start_thread(self, **kwargs):
            expected_args = ["name","auto_archive_duration", "reason"]
            if not valid_kwargs(kwargs,expected_args):  return
            path = BASE + f"/channels/{self,channel_id}/messages/{self.id}/threads"
            kwargs, headers = add_audit_reason(kwargs, self.client_header)
            r = request.post(path, headers=headers,json=kwargs)
            debrief_request(r,self)
            return Channel(**{**r.json,**{"__client__":self.client_header}})

        def join_thread(self):
            path  = BASE + f"/channels/{self.id}/thread-members/@me"
            r = request.put(path, headers=self.client_header)
            debrief_request(r,self)

        def add_thread_member(self, **kwargs):
            expected_args = ["user_id"]
            path = BASE + f"/channels/{self.id}/thread-members/{kwargs['user_id']}"
            r = request.put(path, headers=self.client_header)
            debrief_request(r,self)

        def leave_thread(self, **kwargs):
            path = BASE + f"/channels/{self.id}/thread-members/@me"
            r = request.delete(path, headers=self.client_header)
            debrief_request(r,self)

        def remove_thread_member(self, **kwargs):
            path = BASE + f"/channels/{self.id}/thread-members/{kwargs['user_id']}"
            r = request.delete(path, headers=self.client_header)
            debrief_request(r,self)

        def list_thread_members(self):
            path = BASE + f"/channels/{self.id}/thread-members"
            r = request.get(path, headers=self.client_header)
            debrief_request(r,self)
            return [Thread_Member(**i) for i in r.json()]

        def list_public_archived_threads(self, **kwargs):
            keywords = ["before","limit"]
            path = BASE + f"/channels/{self.id}/threads/archived/public"
            path = process_query(path, keywords,kwargs)
            r = request.get(path, headers=self.client_header)
            debrief_request(r, self)
            arguments = r.json()
            return {"threads":[Channel(**{**arguments['threads'],**{"__client__":self.client_header}})], "members":[Thread_Member(**arguments['members'])], "has_more":boolean(arguments['has_more'])}

        def list_private_archived_threads(self, **kwargs):
            keywords = ["before","limit"]
            path = BASE + f"/channels/{self.id}/threads/archived/private"
            path = process_query(path, keywords,kwargs)
            r = request.get(path, headers=self.client_header)
            debrief_request(r, self)
            arguments = r.json()
            return {"threads":[Channel(**{**arguments['threads'],**{"__client__":self.client_header}})], "members":[Thread_Member(**arguments['members'])], "has_more":boolean(arguments['has_more'])}

        def list_joined_private_archived_threads(self, **kwargs):
            keywords = ["before","limit"]
            path = BASE + f"/channels/{self.id}/users/@me/threads/archived/private"
            path = process_query(path, keywords,kwargs)
            r = request.get(path, headers=self.client_header)
            debrief_request(r, self)
            arguments = r.json()
            return {"threads":[Channel(**{**arguments['threads'],**{"__client__":self.client_header}})], "members":[Thread_Member(**arguments['members'])], "has_more":boolean(arguments['has_more'])}



class Message_Reference:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.message_id = Okwargs["message_id"]
        self.channel_id = Okwargs["channel_id"]
        self.guild_id = Okwargs["guild_id"]
        self.fail_if_not_exists = boolean(Okwargs["fail_if_not_exists"])

class Followed_Channel:
    def __init__(self,**kwargs):
        self.channel_id = kwargs["channel_id"]
        self.webhook_id = kwargs["webhook_id"]

class Reaction:
    def __init__(self,**kwargs):
        self.count = kwargs["count"]
        self.me = boolean(kwargs["me"])
        self.emoji = kwargs["emoji"]

class Overwrite:
    def __init__(self,**kwargs):
        self.id = kwargs["id"]
        self.type = kwargs["type"]
        self.allow = kwargs["allow"]
        self.deny = kwargs["deny"]

class Thread_Metadata:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.archived = boolean(Okwargs["archived"])
        self.auto_archive_duration = Okwargs["auto_archive_duration"]
        self.archive_timestamp = Okwargs["archive_timestamp"]
        self.locked = boolean(Okwargs["locked"])
        self.invitable = boolean(Okwargs["invitable"])

class Thread_Member:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = Okwargs["id"]
        self.user_id = Okwargs["user_id"]
        self.join_timestamp = Okwargs["join_timestamp"]
        self.flags = Okwargs["flags"]

class Embed:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.title = Okwargs["title"]
        self.type = Okwargs["type"] # Don't Use
        self.description = Okwargs["description"]
        self.url = Okwargs["url"]
        self.timestamp = Okwargs["timestamp"]
        self.color = Okwargs["color"]
        self.image = Okwargs["image"]
        self.thumbnail = Okwargs["thumbnail"]
        self.video = Okwargs["video"]
        self.provider = Okwargs["provider"]
        self.author = Okwargs["author"]
        self.footer = Okwargs["footer"]
        self.fields = Okwargs["fields"]


    class Footer:
        def __init__(this,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.text = kwargs["text"]
            self.icon_url = Okwargs["icon_url"]
            self.proxy_icon_url = Okwargs["proxy_icon_url"]

    class Image:
        def __init__(self,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.url = kwargs["url"]
            self.proxy_url = Okwargs["proxy_url"]
            self.height = Okwargs["height"]
            self.width = Okwargs["width"]

    class Thumbnail:
        def __init__(self,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.url = kwargs["url"]
            self.proxy_url = Okwargs["proxy_url"]
            self.height = Okwargs["height"]
            self.width = Okwargs["width"]

    class Video:
        def __init__(self,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.url = Okwargs["url"]
            self.proxy_url = Okwargs["proxy_url"]
            self.height = Okwargs["height"]
            self.width = Okwargs["width"]

    class Provider:
        def __init__(self,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.name = Okwargs["name"]
            self.url = Okwargs["url"]

    class Author:
        def __init__(this,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.name = kwargs["name"]
            self.url = Okwargs["url"]
            self.icon_url = Okwargs["icon_url"]
            self.proxy_icon_url = Okwargs["proxy_icon_url"]

    class Field:
        def __init__(self,**kwargs):
            Okwargs = OptionalKwargs(kwargs)
            self.name = kwargs["name"]
            self.value = kwargs["value"]
            self.inline = boolean(Okwargs["inline"])

class Attachement:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs["id"]
        self.filename = kwargs["filename"]
        self.size = kwargs["size"]
        self.url = kwargs["url"]
        self.proxy_url = kwargs["proxy_url"]
        self.content_type = Okwargs["content_type"]
        self.height = Okwargs["height"]
        self.width = Okwargs["width"]
        self.ephemeral = boolean(Okwargs["ephemeral"])

class Channel_Mention:
    def __init__(self,**kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.id = kwargs["id"]
        self.guild_id = kwargs["guild_id"]
        self.type = kwargs["type"]
        self.name = kwargs["name"]

        channel_types = {0: 'GUILD_TEXT', 1: 'DM', 2: 'GUILD_VOICE', 3: 'GROUP_DM', 4: 'GUILD_CATEGORY', 5: 'GUILD_NEWS', 6: 'GUILD_STORE', 10: 'GUILD_NEWS_THREAD', 11: 'GUILD_PUBLIC_THREAD', 12: 'GUILD_PRIVATE_THREAD', 13: 'GUILD_STAGE_VOICE'}
        self.type_more = OptionalKwargs(channel_types)[self.type]

class Allowed_Mention:
    def __init__(self, **kwargs):
        Okwargs = OptionalKwargs(kwargs)
        self.parse = kwargs["parse"]
        self.roles = kwargs["roles"]
        self.users = kwargs["users"]
        self.replied_user = boolean(kwargs["replied_user"])
