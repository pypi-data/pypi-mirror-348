# imgbyte
Python module for interaction and actions with the imgflip website using a combination of selenium and requests.

# Documentation
## Setup
createWindow()
> Creates a new window and bot instance.<br/>
> Usage:
``` driver = createWindow() ```<br/>
> The driver object will then be used for all future imgbyte functions.<br/>

img_url(driver, page_path)
> Sets the driver window to the input url. Useful if you want to do some custom things with the page html on a specific page. <br/>
> Many of the functions in this module require it, so be aware that use of them will change the window location. <br/>
> imgbyte functions that require this will be notated with a ``` * ```<br/>
> Usage: ``` img_url(driver, 'user/Imgflip') ```<br/>

login(driver, username/email, password)
> Logs into the specified account. <br/>
> Makes use of the get_token function to add the session token to the driver, as ``` driver.token ```. <br/>
> Most functions require being logged into a user account. Ones that do will be notated with a ``` ~ ```. <br/>
> Usage: ``` login(driver, username, password) ```

get_token(driver)
> Returns the current session token as a string. Requires being logged in.
> Optionally, use ```driver.token``` instead.

## Comments
comment_vote(dtiver, vote_type, comment_id) `~`
> Add or Remove and upvote or downvote from a comment.<br/>
> vote_type must be 1 to upvote, 0 to downvote, and -1 to remove your current vote.<br/>
> Usage: ```comment_vote(driver, 1, 1234)``` *Upvotes the comment with id of 1234*

get_comments(driver, post_id) `*`
> Returns a list of comment objects on the post with the given post id.<br/>
> Comment objects have the attributes ```identifier, user, content, postid, user_perm, image```<br/>

> `identifier`: the comment id<br/>
> `user`: username of the user who made the comment<br/>
> `content`: the text of the comment<br/>
> `postid`: the id of the post the comment is on<br/>
> `user_perm`: the permission level of the user. includes ```global-mod, site-mod, stream-mod, normal-user```<br/>
> `image`: if the comment contains an image, this will be a base64 encoded string of said image<br/>

comment_post(driver, post_id, text) `~`
> Comments on the image with the given post id, with the text as the comment content.<br/>
> Returns the response code from the server as a string.<br/>
> Usage: `comment_post(driver, '9geor3', 'This is a comment')`

comment_reply(driver, post_id, comment_id, text) `~` `*`
> Comments a reply to another comment with the given text.<br/>
> Identical usage to `comment_post()` except it additionally requires the id of the comment to reply to.<br/>
> The comment id is typicall obtained with `get_comments()`.

del_own_comment(driver, comment_id) `~`
> Deletes your comment with the given comment id.
> Unlike the `del_comment()` function, it does not require you to be a moderator in the stream the comment is in.

get_basic_comments(driver, post_id) `*`
> Works similarly to the `get_comments()` function, but instead of returning objects with attributes, it returns the comments as a list of html objects.

## Posts
post_vote(driver, vote_type, post_id) `~`
> Upvote, downvote, or remove your vote from a post.<br/>
> vote_type can be 1 for upvote, 0 for downvote, and -1 to remove your current vote.

get_post(driver, post_id) `*`
> Returns the post with the given id as an object.
> Post objects have the following attributes:<br/>

> `identifier`: the post id<br/>
> `author`: the creator of the post<br/>
> `title`: the post's title<br/>
> `desc`: the post's description<br/>
> `tags`: the post's tags (list of strings)<br/>
> `stream`: the stream the post is currently submitted in<br/>
> `image`: base64 encoded string of the post's image<br/>
> If a given attribute does not exist (e.g. there are no tags) it will return with a string labeled ⊙No.(thing), for example:<br/>
> `⊙No.Tags`
> If the post owner is unknown, the owner attribute will be `⊙anonymous`

get_basic_posts(driver, stream, sort) `*`
> Returns all posts on the first page of the given stream as a list of html objects.<br/>
> Sort can either be `hot` or `new`. Leave blank for the stream default.

flag_image(driver, post_id, flag_type, text) `~`
> Flags the image with the given post id.<br/>
> Text is the note that will be given with the flag.<br/>
> Valid options for flag_type are:<br/>
> `img-flag-wrong-stream`: Violates stream rules that aren't disallowed by site TOS<br/>
> `img-nsfw`: NSFW content in image<br/>
> `img-spam`: Post contains excessive copypasta spam or advertising<br/>
> `img-abuse`: Post violates any other part of the imgflip TOS<br/>

create_post(driver, template, stream, title, nsfw, text) `~` `*`
> Create a new post automatically using the imgflip meme generator, and submit it to a specific stream THAT YOU FOLLOW.<br/>
> the template field is the numerical id of the template you want to use. For your own templates, you can find this by going to your profile, My Templates, and select "view template" on the one you wish to view.<br/>
> the NSFW field is either `True` or `False`.<br/>
> For text insertion into the template, imgbyte supports 1 text box being filled. Templates you select must have at least 1 text box, and a maxmimum of one text box may be used, which is always the first one listed on the meme generator page.<br/>
> Usage: `create_post(driver, 1, 'fun', 'This is a title', False, 'This is a text box')`

## Notifications
get_notif_count(driver) `~`
> Returns an integer with the number of notifcations you currently have.

get_notifications(driver) `~` `*`
> WARNING: Use of this function will clear your notifications when used.<br/>
> Note that the way the function is currently set up only works for comment notifications. Any other kind of notification will return with broken strings for the attributes. It is for this reason I recommend changing your account settings to only include comment notifications.<br/>
> Returns a list of notification objects, with the following attributes:<br/>
> `post_id`: The id of the post on which the notification occured<br/>
> `com_id`: The id of the comment that gave the notification<br/>

## Memechat
has_chats(driver) `~`
> Returns either `True` or `False` with whether or not there are currently new unread memechats.

get_unread_memechats(driver) `~` `*`
> Returns a list of unread memechats as objects with the following attributes:<br/>
> `user`: The username of the user who messaged you<br/>
> `time_waiting`: How long ago the user sent the message<br/>
> `text`: The message sent in the memechat. If the message is long enough, it won't display the whole thing.<br/>

get_all_memechats(driver) `~` `*`
> Unlike the unread version this one displays whether a memechat is read or unread, but it does NOT get the actual message that was sent. The object attributes are as follows:<br/>
> `user`: The username of the user who messaged you<br/>
> `time_waiting`: How long ago the user sent the message<br/>
> `status`: either `read` or `unread`. All messages are ordered by most recent.<br/>

post_memechat(driver, user, text) `~` `*`
> Sends a memechat message to the given user. The user must be following you for it to work.<br/>
> Usage: `post_memechat(driver, 'Imgflip', 'This is a memechat message')`

## Moderation
#### Note: All of these require you to be logged in and be a moderator in the stream you're using them in.

ban_user(driver, user, stream, duration, banType) `~` `*`
> Bans the user for preset hour durations.<br/>
> banType must be either `comment` or `post`<br/>

> The `duration` parameter can be any of the following number of hours: 2, 8, 24, 48, -1 (indefinite)<br/>
> Usage: `ban_user(driver, 'Imgflip', 'fun', 8, post)` *Post bans the user Imgflip from fun stream for 8 hours*

alter_post(driver, post_id, title, tags, nsfw, anonymous) `~`
> Edits the post with the given post id<br/>
> `title`, `tags`, `nsfw`, and `anonymous` are optional<br/>
> NOTE: It will set all settings to the given field, so leaving the title field blank for example will set the post's current title to an empty string.<br/>
> `nsfw` and `anonymous` must be either 1 or 0. `anonymous` will set the owner of the post to hidden.<br/>
> Returns the response code from the server

mark_nsfw(driver, post_id) `~` `*`
> Toggles nsfw on the given post. I don't know why you would ever need this, but it's cool that it's here, I guess.
> It was originally supposed to only set the post TO nsfw, but it doesn't and I'm too lazy to change it.

feature(driver, post_id, action, reason, note) `~` `*`
> Feature or Unfeature a post. Works on flagged images as well.<br/>
> `action` can be either 'approve' or 'disapprove'<br/>

> `reason` can be any of the following:<br/>
> `other` (default if none specified)<br/>
> `repost`<br/>
> `political`<br/>
> `spam`<br/>
> `harassment`<br/>
> `abuse` (of TOS)<br/>
> `wrong_stream` (stream-specific rules)<br/>
> `wrong_language` (if the stream has language reqs<br/>

get_comment_flags(driver, stream) `~` `*`
> Gets all flagged comments from the selected stream. Don't use the stream parameter for all streams you moderate.<br/>
> Returns a list of comment objects with the following attributes:<br/>
> `com_id`: the comment's id<br/>
> `post_id`: the id of the post the comment is on<br/>
> `content`: the content of the comment<br/>
> `flagging_user`: the name of the user who flagged the comment<br/>
> `flagged_user`: the username of the comment owner<br/>
> `stream`: the stream the comment is in<br/>
> `link`: the full url link to the comment that was flagged<br/>

get_approval_queue(driver, stream) `~` `*`
> Returns a list of post objects from the approval queue of the given stream. Objects have the following attributes:<br/>
> `identifier`: the post id of the post to approve<br/>
> `owner`: the username of the post's owner<br/>
> `title`: the title of the post<br/>
> `tags`: the tags on the post<br/>

## Misc
get_uid(driver, username)
> Returns the user id number of the user with the given username.
> This is required by a few of the functions, and is useful as although users can change their name, their uid never changes.

follow(driver, uid, follow_type) `~`
> follows the user with the given uid, obtained with `get_uid()`<br/>
> follow type must be 1 for following, and 0 for unfollowing<br/>

Imgflip's post ids are actually integers that are encoded in base 36. The two below functions allow conversion between the two, and are used in many functions that require the use of post ids.

base36_encode(num)
> After inputting an integer, returns the corresponding imgflip post id.

base36_decode(string)
> After inputting an imgflip id, returns the corresponding integer number.

