# Imports
import requests
import re
import time
import threading
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime, timedelta
from typing import Tuple, Callable

# Constants
version = "Selfbot V1.1.0"

base = "chat.jonazwetsloot.nl"
url = f"https://{base}"
api_url = f"{url}/api/v1"
login_url = f"{url}/login"
actionlogin_url = f"{url}/actionlogin"
timeline_url = f"{url}/timeline"
profile_url = f"{url}/users"
inbox_url = f"{url}/inbox"
list_dms_url = f"{url}/messages"
list_group_url = f"{url}/groups"
send_message_url = f"{api_url}/message"
dm_url = f"{api_url}/direct-message"
group_url = f"{api_url}/group-message"
like_url = f"{api_url}/like"
follow_url = f"{api_url}/contact.php"
profile_save_url = f"{api_url}/profile-save"

headers = { 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/json,text/plain,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": base,
    "Origin": url,
    "Referer": login_url,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

# Variables
message_cache = {}
dm_cache = {}
dm_cache_user = {}

show_http = False

# Universal functions:
def check_type(value, class_, argnumber, argname, funcname):
    if value is None:
        args = ", ".join("..." for _ in range(argnumber - 1))
        args = f"{args}, {argname}:{class_.__name__}" if args else f"{argname}:{class_.__name__}"
        show_message(f"Expected arg{argnumber} in {funcname}({args}) (was None)", "Error")
        return False

    if type(value) != class_:
        args = ", ".join("..." for _ in range(argnumber - 1))
        args = f"{args}, {argname}:{class_.__name__}" if args else f"{argname}:{class_.__name__}"
        show_message(f"Expected arg{argnumber} to be class {class_.__name__} instead of {value.__class__.__name__} in {funcname}({args})", "Error")
        return False
    
    if argname.find('id') and class_ == str and value == "0":
        args = ", ".join("..." for _ in range(argnumber - 1))
        args = f"{args}, {argname}:{class_.__name__}" if args else f"{argname}:{class_.__name__}"
        show_message(f"Expected arg{argnumber} in {funcname}({args}) not to be '0', perhaps an issue in your code?", "Error")
        return False
    
    return True

def show_message(message:str=None, mtype:str="Standard"):
    if not check_type(message, str, 1, "message", "show_message"): return
    
    if mtype == "Standard":
        print(f"[{version}] {message}")
    elif mtype == "Error":
        print(f"[{version}] Error: {message}")
    elif mtype == "Http" and show_http:
        print(f"[{version}] Http: {message}")
    elif mtype != "Http":
        show_message(f"Ignored show_message due to invalid mtype ('{mtype}')")

allowed = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
def username_to_id(username:str=None):
    if not check_type(username, str, 1, "username", "ProfileService.username_to_id"): return
    return username
    #return ''.join([char if char in allowed or char == ' ' else '' for char in username]).replace(' ', '-')

def username_to_active_id(session, username:str=None):
    if not check_type(username, str, 1, "username", "ProfileService.username_to_active_id"): return

    if not session.user:
        show_message("Log in before attempting to do HTTP requests!", "Error")
        return
    
    success, response = http_request(session, 'get', f'{list_dms_url}/{username}', None, f"activeUserId From {username}")
    soup = BeautifulSoup(response.text, "html.parser")
    iframe = soup.find('div', id='dm-form')
    if iframe is None:
        show_message("Failed to retrieve activeUserId #1.", "Error")
        return
    
    id = iframe.get('data-contact-id')
    if id is None:
        show_message("Failed to retrieve activeUserId #2.", "Error")
        return
    
    return id

def groupname_to_id(session, groupname:str=None):
    if not check_type(groupname, str, 1, "username", "ProfileService.groupname_to_id"): return

    if not session.user:
        show_message("Log in before attempting to do HTTP requests!", "Error")
        return
    
    success, response = http_request(session, 'get', f'{list_group_url}/{groupname}', None, f"groupId From {groupname}")
    soup = BeautifulSoup(response.text, "html.parser")
    iframe = soup.find('div', id='dm-form')
    if iframe is None:
        show_message("Failed to retrieve groupId #1.", "Error")
        return
    
    id = iframe.get('data-group-id')
    if id is None:
        show_message("Failed to retrieve groupId #2.", "Error")
        return
    
    return id

def get_key(session):
    if not session.user:
        show_message("Log in before attempting to do HTTP requests!", "Error")
        return

    if session.saved_key and session.active_user_id:
        return session.saved_key, session.active_user_id
    
    success, response = http_request(session, 'get', timeline_url, None, "Homepage")
    soup = BeautifulSoup(response.text, "html.parser")
    iframe = soup.find('iframe', id='submit-iframe')
    if iframe is None:
        show_message("Failed to retrieve key #1.", "Error")
        return
    
    key = iframe.get('data-key')
    if key is None:
        show_message("Failed to retrieve key #2.", "Error")
        return
    
    id = iframe.get('data-user-id')
    if id is None:
        show_message("Failed to retrieve key (userId) #3.", "Error")
        return
        
    session.saved_key = key
    session.active_user_id = id
    return session.saved_key, session.active_user_id

def extract_messages(session, html:str=None):
    if not check_type(html, str, 1, "html", "extract_messages"): return

    def parse_message(message_container:Tag=None, parent_id:str=None):
        if not check_type(message_container, Tag, 1, "message_container", "parse_message"): return
        if not parent_id is None:
            if not check_type(parent_id, str, 2, "parent_id", "parse_message"): return

        message_div = None
        if parent_id:
            message_div = message_container
        else:
            message_div = message_container.find('div', class_='message')
        
        if not message_div:
            show_message("Message div doesn't exist!", "Error")
            return None

        bar_div = message_div.find('div', class_='bar')
        if not bar_div:
            show_message("Bar div doesn't exist!", "Error")
            return None

        time_element = bar_div.find('p', class_='friendly-time')
        content_element = message_div.find('div', class_='content')
        user_element = bar_div.find('a', class_='username')
        message_id_element = bar_div.find('button', class_='submit inverted message-menu-share-button')

        message_id = message_id_element['data-id'] if message_id_element else "0"
        content_text = get_text_from_message(content_element)
        markdown_text = get_text_from_message(content_element, True)
        user_text = user_element.text.strip() if user_element else "Unknown"

        time_text = time_element.attrs['data-time'] if time_element else ""
        epoch = 0
        if time_text:
            dt = datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")
            epoch = int(dt.timestamp())

        reactions_container = message_container.find('div', class_='reactions')
        reactions = []
        if reactions_container:
            reactions = [parse_message(reaction_div, message_id) for reaction_div in reactions_container.find_all('div', class_='reaction') if reaction_div]

        return PublicMessage(session, epoch, content_text, markdown_text, user_text, message_id, reactions, parent_id)

    soup = BeautifulSoup(html, 'html.parser')
    messages = [parse_message(message_container) for message_container in soup.find_all('div', class_='message-container')]

    return [msg for msg in messages if msg is not None]

def get_text_from_message(message_div:Tag=None, markdown:bool=False, removemarkdown:bool=False):
    if not check_type(message_div, Tag, 1, "message_div", "get_text_from_message"): return ""
    if not check_type(markdown, bool, 2, "markdown", "get_text_from_message"): return ""
    if not check_type(removemarkdown, bool, 2, "removemarkdown", "get_text_from_message"): return ""

    def handle_node(node:NavigableString|Tag=None):
        if isinstance(node, NavigableString):
            return str(node)

        if not check_type(node, Tag, 1, "node", "handle_node"): return ""

        name = node.name
        classes = node.get("class", [])

        if name == "p":
            raw = node.get_text(strip=True)
            if raw.startswith("### "):
                return f"### {raw[4:]}\n"
            if raw.startswith("## "):
                return f"## {raw[3:]}\n"
            if raw.startswith("# "):
                return f"# {raw[2:]}\n"
            return handle_children(node) + "\n"
        if name == "br":
            return "\n"
        if name == "a" and "mention" in classes:
            return node.get_text()
        if name == "span":
            if "inline-code" in classes:
                content = node.get_text()
                return f"`{content}`" if markdown else content
            if "spoiler" in classes or node.get("class") == [""]:
                content = node.get_text()
                return f"||{content}||" if markdown else content
        if name == "strong":
            only_child = list(node.children)
            if len(only_child) == 1 and isinstance(only_child[0], Tag) and only_child[0].name == "em":
                content = only_child[0].get_text()
                return f"***{content}***" if markdown else content
            else:
                content = handle_children(node)
                return f"**{content}**" if markdown else content
        if name == "em":
            content = handle_children(node)
            return f"*{content}*" if markdown else content
        if name == "ins":
            content = handle_children(node)
            return f"__{content}__" if markdown else content
        if name == "del":
            content = handle_children(node)
            return f"~~{content}~~" if markdown else content
        if name == "blockquote":
            content = handle_children(node)
            return f"> {content.strip()}\n" if markdown else content
        if name == "h1":
            content = handle_children(node)
            return f"# {content.strip()}\n" if markdown else f"{content}\n"
        if name == "h2":
            content = handle_children(node)
            return f"## {content.strip()}\n" if markdown else f"{content}\n"
        if name == "h3":
            content = handle_children(node)
            return f"### {content.strip()}\n" if markdown else f"{content}\n"
        if name == "sub":
            content = handle_children(node)
            return f"-# {content.strip()}\n" if markdown else content
        if name == "div" and "code" in classes:
            content = node.get_text().strip("\n")
            lines = content.splitlines()
            if len(lines) > 1:
                lang = lines[0].strip()
                code = "\n".join(lines[1:])
                return f"```{lang}\n{code}\n```" if markdown else content
            return f"```\n{content}\n```" if markdown else content
        if name == "img":
            return node.get("alt", "")

        return handle_children(node)

    def handle_children(tag):
        return "".join(handle_node(child) for child in tag.children)

    result = handle_children(message_div)
    return result.strip()

def strip_markdown(text: str) -> str:
    if not check_type(text, str, 1, "text", "strip_markdown"): return ""

    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`\n]+`', '', text)
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    text = re.sub(r'\|\|([^|]+)\|\|', r'\1', text)
    text = re.sub(r'^> ?(.*)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^#{1,6} ', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-*+] ', '', text, flags=re.MULTILINE)
    return text.strip()

def http_request(session, type: str = None, url: str = None, data: dict = None, description: str = None, nokey: bool = False):
    method = getattr(session, type.lower())
    if data:
        response = method(url, data=data, headers=headers)
    else:
        response = method(url, headers=headers)

    show_message(f"Response Status Code ({description}): {response.status_code}", "Http")
    return response.status_code < 400, response

# MessageService functions:
def reply(session, message_id:str=None, message:str=None):
    if not check_type(message_id, str, 1, "message_id", "MessageService.reply"): return
    if not check_type(message, str, 2, "message", "MessageService.reply"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return

    data = {
        "message": message,
        "id": message_id,
        "name": session.user,
        "key": key,
        "activeUserId": id
    }
    success, response = http_request(session, 'post', send_message_url, data, "Send Reply")

    message_obj = None
    if success:
        id = response.json().get('id')
        message_obj = PublicMessage(session, time.time(), strip_markdown(message), message, session.user, str(id) if id else "0", [], None)
    return success, message_obj

def like(session, message_id:str=None, value:bool=True):
    if not check_type(message_id, str, 1, "message_id", "MessageService.like"): return
    if not check_type(value, bool, 2, "value", "MessageService.like"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return
    
    data = {
        "id": message_id,
        "like": str(value).lower(),
        "name": session.user,
        "key": key,
        "activeUserId": id
    }

    success, response = http_request(session, 'post', like_url, data, "Like Message")
    return success

def edit(session, message_id:str=None, message:str=None):
    if not check_type(message_id, str, 1, "message_id", "MessageService.edit"): return
    if not check_type(message, str, 2, "message", "MessageService.edit"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return

    data = {
        "message": message,
        "name": session.user,
        "key": key,
        "id": message_id,
        "activeUserId": id
    }
    response = session.put(send_message_url, data=data, headers=headers)
    show_message(f"Response Status Code (Edit Message): {response.status_code}", "Http")

    return response.status_code < 400

def delete(session, message_id:str=None):
    if not check_type(message_id, str, 1, "message_id", "MessageService.delete"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return

    data = {
        "name": session.user,
        "key": key,
        "id": message_id,
        "activeUserId": id
    }
    response = session.delete(send_message_url, data=data, headers=headers)
    show_message(f"Response Status Code (Delete Message): {response.status_code}", "Http")

    return response.status_code < 400

def direct_message(session, username:str=None, message:str=None):
    if not check_type(username, str, 1, "username", "direct_message"): return
    username = username_to_id(username)
    if not check_type(message, str, 2, "message", "direct_message"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return
    
    data = {
        "attachments": "",
        "name": session.user,
        "key": key,
        "activeUserId": id,
        "user": username,
        "message": message
    }

    if session.dm_id_v2:
        userid = username_to_active_id(session, username)
        if not userid:
            return
        data["userId"] = userid

    success, response = http_request(session, 'post', dm_url, data, "Direct Message")
    return success
    
def group_message(session, group_id:str=None, message:str=None):
    if not check_type(group_id, str, 1, "group_id", "group_message"): return
    if not check_type(message, str, 2, "message", "group_message"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return
    
    data = {
        "attachments": "",
        "name": session.user,
        "key": key,
        "activeUserId": id,
        "id": group_id,
        "message": message
    }

    success, response = http_request(session, 'post', group_url, data, "Group Message")
    return success

# ProfileService functions:
def follow(session, username:str=None, value:bool=True):
    if not check_type(username, str, 1, "username", "ProfileService.follow"): return
    if not check_type(value, bool, 2, "value", "ProfileService.follow"): return
    
    key = session.key
    id = session.id
    if not key or not id:
        return
    
    method = value and "POST" or "DELETE"
    data = {
        "user": username,
        "method": method,
        "name": session.user,
        "key": key,
        "activeUserId": id
    }

    success, response = http_request(session, 'post', follow_url, data, "Follow User")
    return success

# Time functions:
def format_real_time(timestr:str):
    if not check_type(timestr, str, 1, "timestr", "format_real_time"): return

    if timestr:
        try:
            time_obj = datetime.strptime(timestr, "%H:%M")
            now = datetime.now()
            
            target_time = now.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
            
            if target_time < now:
                target_time = target_time + timedelta(days=1)

            time_diff = target_time - now
            return int(time_diff.total_seconds())
        except ValueError:
            show_message(f"Invalid DM time format: {timestr}", "Error")
            return 0
    else:
        return 0

    
def format_date(datestr:str):
    if not check_type(datestr, str, 1, "datestr", "format_data"): return

    if datestr == "Today":
        return datetime.today().strftime("%d/%m/%y")
    elif datestr == "Yesterday":
        return (datetime.today() - timedelta(days=1)).strftime("%d/%m/%y")
    else:
        return datestr

# Message classes
class PublicMessage:
    def __init__(self, session, time, text, markdowntext, sender, id, reactions, parent_id):
        self.session = session

        self.time = float(time)     # 0 in old public messages
        self.text = text
        self.markdowntext = markdowntext
        self.sender = sender
        self.id = str(id)

        self.reactions = reactions
        self.parent_id = parent_id

    def like(self, value:bool=True):
        return like(self.session, self.id, value)

    def reply(self, message:str=None):
        return reply(self.session, self.id, message)

    def edit(self, message:str=None):
        return edit(self.session, self.id, message)

    def delete(self):
        return delete(self.session, self.id)

    def bind_to_reply(self, func:Callable=None):
        BotService.ConnectionService.bind_to_message_reply(self.id, func)

class DMMessage:
    def __init__(self, session, time, text, markdowntext, sender, id, groupname):
        self.session = session

        self.time = float(time)     # 0 in any-user dms
        self.text = text
        self.markdowntext = markdowntext
        self.sender = sender
        self.id = str(id)           # "0" in any-user dms
        self.groupname = groupname  # None in normal dms

    def reply(self, message:str=None):
        if self.groupid:
            group_message(self.session, self.groupid, message)
        else:
            direct_message(self.session, self.sender, message)

class Profile:
    def __init__(self, session, username, verified, following, followers, likes, description, markdowndescription, socials, join_date, trophies):
        self.session = session

        self.username = username
        self.verified = verified
        self.following = following
        self.followers = followers
        self.likes = likes
        self.description = description
        self.markdowndescription = markdowndescription
        self.socials = socials
        self.join_date = join_date
        self.trophies = trophies

    def follow(self, value:bool=True):
        follow(self.session, self.username, value)

# Core services
class ConnectionService:
    # Core:
    def __init__(self, session):
        self.session = session

        self.public_functions = []
        self.reply_functions = {}
        self.is_checking_public = False

        self.anydm_functions = []
        self.userdm_functions = {}
        self.is_checking_dms = False

    # Core public:
    def _run_bound_functions(self, message:PublicMessage=None):
        if not check_type(message, PublicMessage, 1, "message", "ConnectionService._run_bound_functions"): return

        if not self.session.check_own and message.sender == self.session.user:
            return

        if self.session.first_run and message.sender == self.session.user:
            return
            
        for func in self.public_functions:
            threading.Thread(target=func, args=(message,), daemon=False).start()

    def _run_bound_functions_to_reply(self, message:PublicMessage=None, parent_id:str=None):
        if not check_type(message, PublicMessage, 1, "message", "ConnectionService._run_bound_functions_to_reply"): return
        if not check_type(parent_id, str, 2, "parent_id", "ConnectionService._run_bound_functions_to_reply"): return

        if not self.session.check_own and message.sender == self.session.user:
            return
        
        if self.session.first_run and message.sender == self.session.user:
            return

        if self.reply_functions.get(parent_id):
            for func in self.reply_functions[parent_id]:
                threading.Thread(target=func, args=(message,), daemon=False).start()

    def _check_periodically_public(self):
        while self.is_checking_public:
            if len(self.public_functions) < 1 and len(self.reply_functions) < 1: return
            try:
                success, response = http_request(self.session, 'get', timeline_url, None, "Homepage")
                if success:
                    messages = extract_messages(self.session, response.text)
                    def handle_message_list(messages, first):
                        for message in messages:
                            if message != None:
                                if time.time() - message.time < 600 and message.id not in message_cache:
                                    message_cache[message.id] = message.time
                                    if first:
                                        self._run_bound_functions(message)
                                    else:
                                        self._run_bound_functions_to_reply(message, message.parent_id)
                                handle_message_list(message.reactions, False)
                            else:
                                show_message("Message is None", "Error")
                    
                    handle_message_list(messages, True)
                else:
                    show_message("Access to Homepage failed/denied", "Error")

                self.check_public_cache()
                self.session.first_run = False
            except Exception as e:
                show_message(f"Error checking for new public posts: {e}", "Error")
            time.sleep(10)

    def check_public_cache(self):
        to_delete = [id for id, unix in message_cache.items() if time.time() - unix > 600]
        for id in to_delete:
            del message_cache[id]

    # Core DM:
    def _run_dm_functions(self, message:DMMessage=None, name:str=None): 
        if not check_type(message, DMMessage, 1, "message", "ConnectionService._run_dm_functions"): return
        if not check_type(name, str, 2, "name", "ConnectionService._run_dm_functions"): return
        global dm_cache

        if not dm_cache.get(name):
            dm_cache[name] = message.markdowntext
        elif dm_cache[name] != message.markdowntext:
            dm_cache[name] = message.markdowntext
            for func in self.anydm_functions:
                threading.Thread(target=func, args=(message,), daemon=False).start()

    def _check_periodically_dms(self):
        while self.is_checking_dms:
            if len(self.anydm_functions) < 1: return
            try:
                success, response = http_request(self.session, 'post', inbox_url, None, "DM Inbox")
                if success:
                    soup = BeautifulSoup(response.text, "html.parser")
                    for user_contact in soup.find_all('a', class_='user-contact'):
                        name = user_contact.find('h3').text.strip()
                        groupname = None
                        newestmessage_element = user_contact.find('p')
                        b = newestmessage_element.find('b')
                        if b:
                            if name != b.text.strip():
                                groupname = name
                            name = b.text.strip()
                            b.decompose()
                        else:
                            continue # to prevent getting own

                        newestmessage = newestmessage_element.text.strip()
                        rawmessage = strip_markdown(newestmessage)
                        if newestmessage == "You have not yet sent any messages to this person." or newestmessage == "No messages have been sent in this group chat yet.":
                            continue

                        global dm_cache
                        if user_contact.find('img', class_='info'):
                            if not dm_cache.get(name):
                                dm_cache[name] = "[empty]"
                            continue

                        self._run_dm_functions(DMMessage(self.session, "0", rawmessage, newestmessage, name, "0", groupname), groupname or name)
                else:
                    show_message("Access to DM Inbox failed/denied", "Error")

                for username, functions in self.userdm_functions.items():
                    success, response = http_request(self.session, 'get', f'{list_dms_url}/{username}', None, f"DMs From {username}")
                    soup = BeautifulSoup(response.text, "html.parser")
                    offset = 0
                    for message_box in soup.find_all('div', class_='receiver'):
                        offset += 1
                        message_box = message_box.find('div', class_='dm')
                        id = message_box['data-id']
                        if dm_cache_user.get(id):
                            continue

                        time_literal = message_box.find('p', class_='time').text.strip()

                        time_day = ""
                        date_span = message_box.find_previous('span', class_='date')
                        if date_span:
                            time_day = date_span.text.strip()
                        else:
                            time_day = "Today"

                        datestr = f"{format_date(time_day)} {time_literal}"
                        unix = int(datetime.strptime(datestr, "%d/%m/%y %H:%M").timestamp()) + offset

                        if time.time() - unix < 600:
                            dm_cache_user[id] = unix

                            name = message_box.find('a', class_='username').text.strip()
                            text = get_text_from_message(message_box.find('div', class_='content'))
                            markdowntext = get_text_from_message(message_box.find('div', class_='content'), True)

                            message = DMMessage(self.session, unix, text, markdowntext, name, id, None)
                            for func in functions:
                                threading.Thread(target=func, args=(message,), daemon=False).start()

                    self._check_dm_cache()
            except Exception as e:
                show_message(f"Error checking for new dm posts: {e}", "Error")
            time.sleep(10)

    def _check_dm_cache(self):
        to_delete = [id for id, unix in dm_cache_user.items() if time.time() - unix > 600]
        for id in to_delete:
            del dm_cache_user[id]

    # Public service:
    def bind_to_public_post(self, func:Callable=None):
        if not callable(func):
            show_message(f"Expected arg1 to be callable in ConnectionService.bind_to_public_post(func:function)", "Error")
            return

        self.public_functions.append(func)

    def bind_to_message_reply(self, message_id:str=None, func:Callable=None):
        if not check_type(message_id, str, 1, "message_id", "ConnectionService.bind_to_message_reply"): return
        if not callable(func):
            show_message(f"Expected arg2 to be callable in ConnectionService.bind_to_message_reply(..., func:function)", "Error")
            return

        if message_id not in self.reply_functions:
            self.reply_functions[message_id] = []
        self.reply_functions[message_id].append(func)

    def start_checking_public(self):
        if not self.is_checking_public:
            self.is_checking_public = True
            threading.Thread(target=self._check_periodically_public, daemon=False).start()

    def stop_checking_public(self):
        self.is_checking_public = False

    # DM Service:
    def bind_to_any_dm(self, func:Callable=None):
        if not callable(func):
            show_message(f"Expected arg1 to be callable in ConnectionService.bind_to_any_dm(func:function)", "Error")
            return
        
        self.anydm_functions.append(func)

    def bind_to_user_dm(self, username:str=None, func:Callable=None):
        if not check_type(username, str, 1, "username", "ConnectionService.bind_to_user_dm"): return
        if not callable(func):
            show_message(f"Expected arg2 to be callable in ConnectionService.bind_to_user_dm(.., func:function)", "Error")
            return

        username = username.replace(' ', '-')
        if username not in self.userdm_functions:
            self.userdm_functions[username] = []
        self.userdm_functions[username].append(func)

    def start_checking_dms(self):
        if not self.is_checking_dms:
            self.is_checking_dms = True
            threading.Thread(target=self._check_periodically_dms, daemon=False).start()

    def stop_checking_dms(self):
        self.is_checking_dms = False

class MessageService:
    def __init__(self, session):
        self.session = session

    def create_post(self, message:str=None) -> Tuple[bool, str]:
        if not check_type(message, str, 1, "message", "MessageService.create_post"): return
    
        key = self.session.key
        id = self.session.id
        if not key or not id:
            return

        data = {
            "message": message,
            "attachments": "",
            "name": self.session.user,
            "key": key,
            "activeUserId": id
        }
        success, response = http_request(self.session, 'post', send_message_url, data, "Send Message")

        message_obj = None
        if success:
            id = response.json().get('id')
            message_obj = PublicMessage(self.session, time.time(), strip_markdown(message), message, self.session.user, str(id) if id else "0", [], None)
        return success, message_obj

    def reply(self, message_id:str=None, message:str=None) -> Tuple[bool, str]:
        return reply(self.session, message_id, message)

    def like(self, message_id:str=None, value:bool=True) -> Tuple[bool, str]:
        return like(self.session, message_id, value)

    def edit(self, message_id:str=None, message:str=None) -> bool:
        return edit(self.session, message_id, message)

    def delete(self, message_id:str=None):
        return delete(self.session, message_id)

    def direct_message(self, username:str=None, message:str=None) -> bool:
        return direct_message(self.session, username, message)

    def get_group_id_by_name(self, group_name:str=None) -> str:
        if not check_type(group_name, str, 1, "group_name", "MessageService.get_group_id_by_name"): return
        return groupname_to_id(self.session, group_name)

    def message_group_by_name(self, group_name:str=None, message:str=None) -> bool:
        group_id = self.get_group_id_by_name(group_name)
        if group_id:
            return group_message(self.session, group_id, message)

    def message_group_by_id(self, group_id:str=None, message:str=None) -> bool:
        return group_message(self.session, group_id, message)

class ProfileService:
    def __init__(self, session):
        self.session = session
        self.profile_cache = {}

        threading.Thread(target=self._periodically_clear_cache, daemon=False).start()

    def get_profile(self, username:str=None):
        if not check_type(username, str, 1, "username", "ProfileService.get_profile"): return
        username = username_to_id(username)
        if username == username_to_id(self.session.user):
            show_message("Can't get your own profile!", "Error")
            return # Can't get own profile for now
        
        cache = self.profile_cache.get(username)
        if cache: return cache

        response = self.session.post(f"{profile_url}/{username}", headers=headers)
        show_message(f"Response Status Code (Get Profile): {response.status_code}", "Http")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            account_info_div = soup.find('div', id='account-info')
            if not account_info_div:
                return
            
            username_div = account_info_div.find('div', id='username')
            username = username_div.find('h1').text.strip()
            verified = username_div.find('h1').find('img') is not None
            following = int(username_div.find('span', id='following-count').text.strip()) or 0
            followers = int(username_div.find('span', id='follower-count').text.strip()) or 0
            likes = int(username_div.find('span', id='like-count').text.strip()) or 0
            description = get_text_from_message(soup.find('div', id='description'))
            markdowndescription = get_text_from_message(soup.find('div', id='description'), True)
            socials = {}
            if soup.find('div', id='socials'):
                for social in soup.find('div', id='socials').children:
                    socialtype = social.find('img').get('src').split('/')[-1].replace('.svg', '')
                    socials[socialtype] = social.get('href')
            join_date = soup.find('p', id='signup-date').text.strip().split(' ')[2]
            trophies = []
            for trophy in soup.find('div', id='trophy-container'):
                trophies.append(trophy.find('h3').text.strip())

            profile_obj = Profile(username, verified, following, followers, likes, description, markdowndescription, socials, join_date, trophies)
            self.profile_cache[username] = [time.time(), profile_obj]
            return profile_obj
        
    def set_description(self, description: str):
        if not check_type(description, str, 1, "description", "ProfileService.set_description"): return

        data = {
            'name': self.session.user,
            'key': self.session.key,
            'activeUserId': self.session.id,
            'description': description
            }

        response = self.session.post(profile_save_url, data=data, headers=headers)
        show_message(f"Response Status Code (Profile Description): {response.status_code}", "Http")

    def verify(self) -> bool:
        success = self.session.bot.MessageService.direct_message("Bjarnos", "Verified")[0]
        return success

    def get_trophies(self):
        print('later')
        
    def clear_cache(self):
        self.profile_cache = {}

    def _periodically_clear_cache(self):
        while True:
            time.sleep(300)
            now = time.time()
            keys_to_remove = [key for key, data in self.profile_cache.items() if data[1] < now - 300]
            for key in keys_to_remove:
                del self.profile_cache[key]

    def username_to_id(self, username:str=None):
        return username_to_id(username)
    
    def follow(self, username:str=None, value:bool=True):
        follow(username, value)

class Bot:
    def __init__(self):
        # Necessary
        self.session = requests.session()
        self.session.user = None
        self.session.key = None
        self.session.saved_key = None
        self.session.active_user_id = None

        # Flags
        self.session.first_run = True
        self.session.check_own = True
        self.session.dm_id_v2 = False

        self.session.bot = self

        self.ConnectionService = ConnectionService(self.session)
        self.MessageService = MessageService(self.session)
        self.ProfileService = ProfileService(self.session)

    def login(self, username:str=None, password:str=None, flags:dict=None) -> bool:
        if not check_type(username, str, 1, "username", "Bot.login"): return
        if not check_type(password, str, 2, "password", "Bot.login"): return

        success, response = http_request(self.session, 'get', login_url, None, "Get Token")

        if flags:
            if flags.get('check-own') == False:
                self.session.check_own = False
            if flags.get('force-first') == True:
                self.session.first_run = False
            if flags.get('dm-id-v2') == True:
                self.session.dm_id_v2 = True

        logindata = {"user": username, "pass": password, "redirect": ""}
        response = self.session.post(actionlogin_url, data=logindata, headers=headers)
        show_message(f"Response Status Code (Login): {response.status_code}", "Http")

        if response.status_code != 200:
            return False
        
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find('div', id='page'):
            self.session.user = username
            self.session.key, self.session.id = get_key(self.session)
            return True
        else:
            return False

class ExportBotService:
    def create_bot(self):
        return Bot()
    
    def toggle_show_http(self, value:bool=True):
        if not check_type(value, bool, 1, "value", "BotService.toggle_show_http"): return
        global show_http
        show_http = value
        return value

show_message("Library succesfully loaded.")

class ExportClasses:
    def __init__(self):
        self.Bot = Bot
        self.PublicMessage = PublicMessage
        self.DMMessage = DMMessage
        self.Profile = Profile

BotService = ExportBotService()
Classes = ExportClasses()