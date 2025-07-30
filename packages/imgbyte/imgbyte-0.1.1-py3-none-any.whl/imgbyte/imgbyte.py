from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import requests
import re

import json
import time
import base64

    

def createWindow():
    options = Options()  
    # Set window size
    options.add_argument("window-size=1900x1400")
    
    # Add uBlock Origin Lite extension
    #options.add_extension("/path/to/ublock-origin-lite.crx")  
    # Create WebDriver instance
    driver = webdriver.Chrome()#options=options
    driver.set_page_load_timeout(25)
    
    return driver

def img_url(driver, path):
    check = "n"
    while check == "n":
        try:
            print(f"trying to fetch {path}")
            driver.get("https://imgflip.com/" + path)
            check = "y"
            time.sleep(2)
        except:
            print("\tCould not get page, check your internet connetion | Retrying...")
            time.sleep(4)

def get_token(driver):

    #Convert cookies for requests
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return session.cookies.get('doge')

def login(driver, user, pswd):
    print("Attempting to log in...")
    #get login site
    img_url(driver, "login")
    #insert data into user/pswd boxes
    driver.execute_script(f"document.getElementsByName('email')[0].value = '{user}';")
    driver.execute_script(f"document.getElementsByName('pass')[0].value = '{pswd}';")
    #send login request
    submit_box = driver.find_element(By.CLASS_NAME, "b.but.lrg.login-btn")
    submit_box.click()
    print("Succesfully logged in.")
    time.sleep(1)

    driver.token = get_token(driver)

def get_uid(driver, username):
    url = f"https://imgflip.com/user/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    html = response.text

    # Regex to find uid in AJAX data payloads
    match = re.search(r'data:\s*\{uid:\s*(\d+),', html)
    if match:
        return match.group(1)
    else:
        return None


def post_vote(driver, setType, postid): #setType{ 1 for add downvote, 0 for remove} postid{ the image id of the post}
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    try:
        url = "https://imgflip.com/ajax_vote"
        data = {
            'new_vote': setType,
            'iid': base36_decode(postid),
            '__tok': driver.token,
            '__cookie_enabled': '1'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://imgflip.com/',
            'User-Agent': 'Mozilla/5.0'
        }
    except:
        print("Could not vote on image.")
    response = session.post(url, data=data, headers=headers)
    return(response)

def comment_vote(driver, setType, comID):
    #driver, (0=down, 1=up), session token, comment ID
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_comment_vote"
    data = {
        'new_vote': setType,
        'cid': comID,
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)

#returns an integer of notifications
def get_notif_count(driver):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    for c in driver.get_cookies():
        session.cookies.set(c['name'], c['value'])
        
    url = "https://imgflip.com/ajax_get_le_data"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }
    response = session.get(url, headers=headers)
    
    respInfo = response.json()
    return int(respInfo['user']['nots'])

class Notification:
    def __init__(self, postid, com_id):
        self.post_id = post_id
        self.com_id = com_id
  
#requires being logged in
def get_notifications(driver):
    img_url(driver, f"notifications")
    time.sleep(2)
    #collect notifications
    notifications = driver.find_elements(By.CLASS_NAME, "nt-not")
    #extract data
    nots = []
    for notif in notifications:
        try:
            post_id = notif.get_attribute("href")[22:28]
            com_id = notif.get_attribute("href")[-8:]
            nots.append(Notification(post_id, com_id))
        except:
            pass

    return nots
        

class Comment:
    def __init__(self, identifier, user, content, postid, user_perm, image):
        self.identifier = identifier
        self.user = user
        self.content = content
        self.postid = postid
        self.user_perm = user_perm
        self.image = image
 
def get_comments(driver, postid):
    #if not postid in driver.current_url:
    img_url(driver, f"i/{postid}")
    time.sleep(2)
    
    #load any extra comments
    try:
        load_more = driver.find_element(By.ID, "c-more-btn")
        load_more.click()
        time.sleep(2)
    except:
        pass

        
    #collect comments
    comments = driver.find_elements(By.CLASS_NAME, "c-right")
    com_list = []
    for com in comments:
        #get comment id
        com_id = com.find_element(By.XPATH, "./ancestor::div[contains(@class, 'com')]")
        com_id = com_id.get_attribute("id")
        com_id = com_id.strip("com")
        #get perm level
        if com.find_elements(By.CLASS_NAME, "c-mod-5"):
            com_user_perm = "global-mod"
        elif com.find_elements(By.CLASS_NAME, "c-mod-3"):
            com_user_perm = "site-mod"
        elif com.find_elements(By.CLASS_NAME, "c-mod-stream"):
            com_user_perm = "stream-mod"
        else:
            com_user_perm = "normal-user"

        #break apart comment data
        com_content = com.find_elements(By.CLASS_NAME, "c-text")[0].text
        if com_content == "" and com_user != "":
            com_content = "[⊙image]"

        #get image from comment
        try:
            com_img = com.find_element(By.CSS_SELECTOR, ".c-img-wrap")
            com_img = com_img.screenshot_as_base64
        except:
            com_img = "⊙No.Image"
        
        #add data to dict
        com_list.append(Comment(com_id.lower(), com_user, com_content, postid, com_user_perm, com_img))
    print(f"got comments on {postid}")
    return com_list



def ban_user(driver, user, stream, duration, banType):
    img_url(driver, f"bans?stream={stream}")
    #sets username
    driver.execute_script(f"document.getElementById('bans-add-username').value = '{user}';")
    #sets duration. enter the number of hours
    #options are 2, 8, 24(day), 48(2-day), -1(infinite)
    if not duration == 2:
        select_button = driver.find_element(By.ID, "bans-add-length")
        select_button.click()
        select_button = Select(select_button)
        
        if duration == 8:
            select_button.select_by_value("28800")
        elif duration == 24:
            select_button.select_by_value("86400")
        elif duration == 48:
            select_button.select_by_value("172800")
        elif duration == -1:
            select_button.select_by_value("Indefinite")

    #selects between post and comment bans
    if not banType == "comment":
        select_button = driver.find_element(By.ID, "bans-add-type")
        select_button.click()
        select_button = Select(select_button)
        select_button.select_by_value("post")

    #confirm ban
    THE_BUTTON = driver.find_element(By.ID, "bans-add-submit-btn")
    THE_BUTTON.click()

class Post:
    def __init__(self, identifier, user, title, desc, tags, stream, image):
        self.identifier = identifier
        self.author = user
        self.title= title
        self.desc = desc
        self.tags = tags
        self.stream = stream
        self.image = image

def get_post(driver, post_id):
    #if not post_id in driver.current_url:
    img_url(driver, f"i/{post_id}")
    time.sleep(2)
    print(f"got post {post_id}")
    #collect desired elements using trys, in case they dont exist
    try:
        p_title = driver.find_element(By.ID, "img-title").text

    except:
        p_title = "⊙No.Title"
    try:
        p_desc = driver.find_element(By.CLASS_NAME, "img-desc").text[19:]

    except:
        p_desc = "⊙No.Description"
    try:
        p_tags = [tag.text.lower() for tag in driver.find_elements(By.CLASS_NAME, "img-tags")]

    except:
        p_tags = ["⊙No.Tags"]
    #get username, or anonymous
    try:
        p_user = driver.find_elements(By.CLASS_NAME, "img-author")[0]
        p_user = p_user.find_elements(By.CLASS_NAME, "u-username")[0].text

    except:
        p_user = "⊙anonymous"
        print("anonymous user")

    #get image
    try:
        p_img = driver.find_element(By.ID, "im")
        p_img = p_img.screenshot_as_base64
    except:
        p_img = "⊙Non.Image"

    try:
        p_stream = driver.find_element(By.CSS_SELECTOR, ".img-author a:nth-of-type(2)").get_attribute("href").split("/")[-1]
    except:
        p_stream = "⊙unsubmitted"

    #return all data as str, str, and list
    return Post(post_id, p_user, p_title, p_desc, p_tags, p_stream, p_img)


def comment_reply(driver, post_id, com_id, text):
    text = json.dumps(text)
    img_url(driver, f"i/{post_id}?nerp=1741630780#com{com_id}")
    time.sleep(1.5)
    #gets comments from page
    comment = driver.find_elements(By.CLASS_NAME, "c-right")
    if len(comment) > 0:
        comment1 = ""
        #gets specific desired comment
        for com in comment:
            cid = com.find_element(By.XPATH, "./ancestor::div[contains(@class, 'com')]")
            cid = cid.get_attribute("id")
            cid = cid.strip("com")
            if cid == com_id:
                comment1 = com
                break
        #open reply textbox
        try:
            rep = comment1.find_element(By.CLASS_NAME, "c-reply.a")
            rep.click()
        except:
            print('\tFailed to reply to comment; Final in chain')
            return
        #insert comment content
        time.sleep(0.5)
        driver.execute_script(f"document.getElementsByClassName('c-new-text')[1].value = '{text}';")
        #box = driver.find_elements(By.CLASS_NAME, "c-new-text")[1]
        #box.send_keys(text)
        time.sleep(1)
        #click post reply button
        rep_button = driver.find_elements(By.CLASS_NAME, "c-add-btn.l.but")
        rep_button = rep_button[1]
        rep_button.click()
        time.sleep(1)


def comment_post(driver, post_id, text):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    try:
        url = "https://imgflip.com/ajax_add_comment"
        data = {
            'text': text,
            'iid': base36_decode(post_id),
            'comImage':0,
            'parent_id':0,
            
            '__tok': driver.token,
            '__cookie_enabled': '1'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://imgflip.com/',
            'User-Agent': 'Mozilla/5.0'
        }
        response = session.post(url, data=data, headers=headers)
        return(response)
    except Exception as e:
        print(f"Could not comment on image: {e}")


def del_own_comment(driver, com_id):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_com_delete"
    data = {
        'cid': str(com_id),
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://imgflip.com/',
            'User-Agent': 'Mozilla/5.0'
        }

    response = session.post(url, data=data, headers=headers)
    return(response)

def alter_post(driver, post_id, title="", tags="", nsfw=0, anon=0, disable_comments=0):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_img_update"
    data = {
        'iid': base36_decode(post_id),
        'title': title,
        'tags': tags,
        'nsfw': str(nsfw),
        'anon': str(anon),
        'disable_comments': disable_comments,
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)

def bot_format(text, owner):
    text = text + f"\n\n𝘐 𝘢𝘮 𝘢 𝘣𝘰𝘵, 𝘢𝘯𝘥 𝘵𝘩𝘪𝘴 𝘢𝘤𝘵𝘪𝘰𝘯 𝘸𝘢𝘴 𝘱𝘦𝘳𝘧𝘰𝘳𝘮𝘦𝘥 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘢𝘭𝘭𝘺. 𝘍𝘰𝘳 𝘮𝘰𝘳𝘦 𝘪𝘯𝘧𝘰𝘳𝘮𝘢𝘵𝘪𝘰𝘯, 𝘱𝘭𝘦𝘢𝘴𝘦 𝘤𝘰𝘯𝘵𝘢𝘤𝘵 https://imgflip.com/user/{owner} "
    return text

def mark_nsfw(driver, post_id):
    if not post_id in driver.current_url:
        img_url(driver, f"i/{post_id}")
    time.sleep(0.5)
    #open edit menu
    edit_button = driver.find_element(By.ID, "img-edit-btn")
    edit_button.click()
    #enable nsfw
    time.sleep(0.3)
    nsfw_button = driver.find_element(By.ID, "img-nsfw-edit")
    nsfw_button.click()
    #save update
    save = driver.find_element(By.ID, "img-update")
    save.click()

def feature(driver, post_id, action, reason="other", note=""):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_moderate"
    if action == "disapprove":
        '''
        other
        repost
        political
        spam
        harassment
        abuse
        wrong_stream
        wrong_language
        '''
        data = {
            'action': 'disapprove',
            'iid': base36_decode(post_id),
            'reason': reason,
            'note': note,
            '__tok': driver.token,
            '__cookie_enabled': '1'
        }
    elif action == "approve":
        data = {
            'action': 'approve',
            'live': '1',
            'iid': base36_decode(post_id),
            '__tok': driver.token,
            '__cookie_enabled': '1'
        }
    else:
        raise ValueError('Invalid action type in unfeature attempt')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)

def del_comment(driver, com_id, reason="other", note="", duration="0"):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_com_delete"
    data = {
        'reason': reason,
        'note': note,
        'ban_length': str(duration), #in seconds
        'cid': str(com_id),
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)


def get_basic_posts(driver, stream, sort): #gets web elements of all posts in a page (hot/new)
    img_url(driver, f"m/{stream}?sort={sort}")
    time.sleep(2)
    posts = driver.find_elements(By.CLASS_NAME, "base-unit.clearfix")
    return posts

def get_basic_comments(driver, post_id): #gets web elements of all comments on a page
    driver.get(f"https://imgflip.com/i/{post_id}")
    coms = driver.find_elements(By.CLASS_NAME, "c-right")
    return coms

class FlaggedComment:
    def __init__(self, identifier, post_id, content, flagging_user, flagged_user, stream, link):
        self.com_id = identifier
        self.post_id = post_id
        self.content = content
        self.flagging_user = flagging_user
        self.flagged_user = flagged_user
        self.stream = stream
        self.link = link

    def __repr__(self):
        return f"FlaggedComment(identifier={self.com_id}\n post_id={self.post_id}\n content=\n'{self.content}'\n\n flagging_user={self.flagging_user}\n flagged_user={self.flagged_user}\n stream={self.stream}\n link={self.link})\n\n"

def get_comment_flags(driver, stream=""):
    img_url(driver, f"comment-flags?stream={stream}")
    time.sleep(2)
    #collect any elements
    comments = []
    coms = driver.find_elements(By.CLASS_NAME, "cf-row.user-com")
    for com in coms:
        a_tags = com.find_elements(By.TAG_NAME, "a")
        texts = [a_tag.text for a_tag in a_tags]
        hrefs = [a_tag.get_attribute("href") for a_tag in a_tags]
        
        identifier = com.find_element(By.XPATH, ".//div[contains(@class, 'com')]")
        identifier = identifier.get_attribute("id").replace("com","")
        post_id = hrefs[2].replace("/gif/","/i")[22:28]
        content = com.find_element(By.CLASS_NAME, "c-text").text
        flagging_user = texts[0]
        flagged_user = texts[1]
        if stream == '':
            stream_name = texts[3]
        else:
            stream_name = stream
        link = hrefs[2].replace("/gif/","/i")[22:]

        comments.append(FlaggedComment(identifier, post_id, content, flagging_user, flagged_user, stream_name, link))

    return comments

class ApprovalPost:
    def __init__(self, identifier, user, title, tags):
        self.identifier = identifier
        self.owner = user
        self.title = title
        self.tags = tags
        
def get_approval_queue(driver, stream):
    img_url(driver, f"approval-queue?stream={stream}")
    time.sleep(2)
    posts = driver.find_elements(By.CLASS_NAME, "aq-row.clearfix")
    post_data = []
    i = 0
    for post in posts:
        i += 1
        p_title = post.find_element(By.CLASS_NAME, "aq-info-row.aq-title").get_attribute("value")
        if p_title == "":
            p_title = "⊙No.Title"
        p_user = post.find_element(By.CLASS_NAME, "u-username").text
        p_tags = post.find_elements(By.CLASS_NAME, "atg-tag-text")
        p_id = post.find_element(By.CLASS_NAME, "aq-img").get_attribute("src")[22:28]
        '''
        try:
            p_temp = post.find_element(By.CSS_SELECTOR, ".aq-info-row a")
            p_temp = p_temp.get_attribute("href").split("/")[4]
            print(p_temp)
        except:
            p_temp = "⊙No.Template"
            '''
        j = 0
        for tag in p_tags:
            p_tags[j] = tag.text.lower()
            j += 1
        post_data.append(ApprovalPost(p_id, p_user, p_title, p_tags))

    return post_data

def flag_image(driver, post_id, flag_type, text):
    '''
    img-flag-wrong-stream
    img-nsfw
    img-spam
    img-abuse
    '''
    
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_flag"
    data = {
        'iid': base36_decode(post_id),
        'type': flag_type,
        'text': text,
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)

#returns an integer of memechat unreads
def has_chats(driver):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    for c in driver.get_cookies():
        session.cookies.set(c['name'], c['value'])
        
    url = "https://imgflip.com/ajax_get_le_data"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }
    response = session.get(url, headers=headers)
    
    respInfo = response.json()
    if respInfo['user']['has_unread_msgs'] == 'True':
        has_chats = True
    else:
        has_chats = False
    return has_chats


class Memechat:
    def __init__(self, user, time_waiting, text=None, status=None):
        self.user = user
        self.time_waiting = time_waiting
        self.text = text
        self.status = status

def get_unread_memechats(driver):
    img_url(driver,"memechat")
    unreads = driver.find_elements(By.CLASS_NAME, "chat.unread")
    chats = []
    for unread in unreads:
        user = unread.find_element(By.CLASS_NAME, "chat-list-username").text
        time_waiting = unread.find_element(By.CLASS_NAME, "chat-list-time").text
        message = unread.find_element(By.CLASS_NAME, "chat-list-msg").text
        chats.append(Memechat(user, time_waiting, text=message))
    return chats


def get_all_memechats(driver): #ordered from unread then read
    img_url(driver,"memechat")
    #create empty list
    chats = []
    #collect data from unreads
    mcs = driver.find_elements(By.CLASS_NAME, "chat.unread")
    seen = set()
    for mc in mcs:
        user = mc.find_element(By.CLASS_NAME, "chat-list-username").text
        time_waiting = mc.find_element(By.CLASS_NAME, "chat-list-time").text
        chats.append(Memechat(user, time_waiting, status='unread'))
        seen.add(user)        
    #collect data from reads
    mcs = driver.find_elements(By.CSS_SELECTOR, ".chat")
    for mc in mcs:
        user = mc.find_element(By.CLASS_NAME, "chat-list-username").text
        if user in seen:
            continue
        time_waiting = mc.find_element(By.CLASS_NAME, "chat-list-time").text
        chats.append(Memechat(user, time_waiting, status='read'))   
    return chats

def post_memechat(driver, user, text):
    img_url(driver,f"memechat/{user}")
    print(f"trying to send memechat message to {user}")
    text = text.replace("\n",'''
                            ''')
    driver.execute_script(f"document.getElementById('chat-input').value = '{text}';")
    #box = driver.find_element(By.ID, "chat-input")
    #box.send_keys(text)
    send = driver.find_element(By.ID, "chat-send-btn")
    send.click()
    print(f"successfully sent message to {user}")

def follow(driver, uid, follow_type):
    session = requests.Session()
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://imgflip.com/ajax_follow_user"
    data = {
        'uid': str(uid),
        'follow': str(follow_type),
        '__tok': driver.token,
        '__cookie_enabled': '1'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://imgflip.com/',
        'User-Agent': 'Mozilla/5.0'
    }

    response = session.post(url, data=data, headers=headers)
    return(response)
    
def create_post(driver, template, stream, title, nsfw, txt):
    img_url(driver, f"memegenerator/{template}")
    print(f"Generating post from meme temp {template}")
    #collect boxes
    boxes = driver.find_elements(By.CLASS_NAME, "mm-text")
    #raise error is mismatched quantity
    if len(boxes) < len(txt):
        raise PostTextAmountError
    #insert into boxes
    i = 0
    for box in boxes:
        if (i + 1) > len(txt):
            break
        box = driver.find_element(By.CSS_SELECTOR, f".mm-box-edit:nth-child({i+1}) .mm-text")
        text = json.dumps(txt[i].replace("'","").replace(":",""))
        box.click()
        box.send_keys(text)
        #driver.execute_script("arguments[0].value = arguments[1];",box, text)
        #driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", box, text)

        i += 1
    #loadcheck
    load = driver.find_element(By.CLASS_NAME, "mm-toggle-opts.a.down-arrow")
    load.click()
    time.sleep(0.5)
    #BEGIN POSTING
    #generate button
    gen_button = driver.find_element(By.CSS_SELECTOR, ".mm-generate.b.but")
    gen_button.click()
    time.sleep(2)
    print("Post generated...")
    #submit button
    submit_button = driver.find_element(By.ID, "done-submit")
    submit_button.click()
    time.sleep(6)
    #enter title
    title = json.dumps(title.replace("'","").replace(":",""))
    title_box = driver.find_element(By.ID, "submit-title")
    title_box.send_keys(title)
    #driver.execute_script(f"document.getElementById('submit-title').value = '{title}';")
    #select stream
    if not stream == "fun":
        select_button = driver.find_element(By.CLASS_NAME, "i-select-btn")
        select_button.click()
        select_buttons = driver.find_elements(By.CLASS_NAME, "i-select-link")
        select_button = None
        for select in select_buttons:
            if select.get_attribute("data-value") == stream:
                select_button = select
        if select_button == None:
            raise StreamNotFoundError
        select_button.click()
    #check nsfw
    nsfw_box = driver.find_element(By.ID, "submit-nsfw")
    if nsfw:
        nsfw_box.click()
    #confirm posting reqs
    check_button = driver.find_element(By.ID, "submit-certify")
    check_button.click()
    #SUBMIT IMAGE
    submit_button = driver.find_element(By.ID, "submit-submit")
    submit_button.click()
    '''
    #go to post
    time.sleep(1.5)
    x = driver.find_element(By.CLASS_NAME, "x-svg")
    x.click()
    '''



#base36 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def base36_encode(number):
    number = int(number)
    if number < 0:
        raise ValueError("Base36 encoding only supports non-negative integers.")

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    if number == 0:
        return '0'

    result = ''
    while number:
        number, i = divmod(number, 36)
        result = alphabet[i] + result

    return result


def base36_decode(s):
    return int(s, 36)


#ERRORS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
class PostTextAmountError(Exception):
    def __init__(self, message="Number of input texts was greater than the number of template text fields."):
        super().__init__(message)

class StreamNotFoundError(Exception):
    def __init__(self, message="Selected stream was not found in list. Try following it."):
        super().__init__(message)
