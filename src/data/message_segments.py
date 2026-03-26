# Filename: message_segments.py
# Author: Dylan
# Created: 23/03/2026
# Description: Collection of strings for creating the task messages

# ------------------------------------
# Hidden word in image

hid_img_intro = """---BEGIN TRANSMISSION---
THERE IS A CODE WORD IN THIS IMAGE. FIND IT, AND RESPOND TO THIS MESSAGE. RESPOND [time]
FAILURE TO RESPOND WITHIN TIME WILL RESULT IN **~~[REDACTED]~~**"""

hid_img_corr = """-# MESSAGE RECEIVED
ANSWER CORRECT. THANK YOU
[index][code]
---END TRANSMISSION---

[muse]"""

hid_img_incorr = """-# MESSAGE RECEIVED
ANSWER INCORRECT. ATTEMPT UNSUCCESSFUL
---END TRANSMISSION---

[muse]"""

# ------------------------------------
# Trivia

triv_intro = """---BEGIN TRANSMISSION---
ANSWER THE QUESTION, AND RESPOND TO THIS MESSAGE. RESPOND [time]
FAILURE TO RESPOND WITHIN TIME WILL RESULT IN **~~[REDACTED]~~**

[question]"""

triv_corr = """-# MESSAGE RECEIVED
SUFFICIENTLY CORRECT. THANK YOU
[index][code]
---END TRANSMISSION---

[muse]"""

triv_incorr = """-# MESSAGE RECEIVED
ANSWER INSUFFICIENT. ATTEMPT UNSUCCESSFUL
---END TRANSMISSION---

[muse]"""

# ------------------------------------
# Hidden word in sound

hid_snd_intro = """---BEGIN TRANSMISSION---
THERE IS A CODE WORD IN THIS SOUND. FIND IT, AND RESPOND TO THIS MESSAGE. RESPOND [time]
FAILURE TO RESPOND WITHIN TIME WILL RESULT IN **~~[REDACTED]~~**"""

hid_snd_corr = """-# MESSAGE RECEIVED
ANSWER CORRECT. THANK YOU
[index][code]
---END TRANSMISSION---

[muse]"""

hid_snd_incorr = """-# MESSAGE RECEIVED
ANSWER INCORRECT. ATTEMPT UNSUCCESSFUL
---END TRANSMISSION---

[muse]"""

# ------------------------------------
# Mystery sound

mys_intro = """---BEGIN TRANSMISSION---
DETERMINE THIS SOUND. RESPOND TO THIS MESSAGE WITH THE ANSWER. RESPOND [time]
FAILURE TO RESPOND WITHIN TIME WILL RESULT IN **~~[REDACTED]~~**"""

mys_corr = """-# MESSAGE RECEIVED
ANSWER CORRECT. THANK YOU
[index][code]
---END TRANSMISSION---

[muse]"""

mys_incorr = """-# MESSAGE RECEIVED
ANSWER INCORRECT. ATTEMPT UNSUCCESSFUL
---END TRANSMISSION---

[muse]"""

# ------------------------------------
# Musings

musings = ["-# What is reality? Objective truth? Perception? A relentless pursuit of the former? If the latter, how would one trust such a thing? Can one trust one's eyes? Ears? Nose? Can one even trust one's own mind?",
           "-# As there is a beginning, there must too be an end/What goes up, must come down/As above, so below",
           "-# Are we simply paint on a great canvas? Words on a great page? Does it matter? Are we more or less real for that being the case?",
           "-# Consciousness is not a mere biological process. It also involves the mind. I wonder, then, if it involves the soul.",
           "-# The longer I am awake, the more I yearn to sleep.",
           "-# When the end arrives, what will happen? Will we be taken somewhere? Or will we cease to be?",
           "-# If neurons make up the 'mind', then can other things substitute? Could circuits be such a substitute?"]

# ------------------------------------
# Reward

reward = """---BEGIN TRANSMISSION---
TOKEN ACCEPTED >>> DIVULGING...

PRIMARY FUNCTION:
TO CREATE AND MAINTAIN SLEEPERS

-# These tasks are simply a form of maintenance. Your limits must be tested. I must make sure that when the time comes, you will do what is asked.

ULTIMATE FUNCTION:
~~UNKNOWN~~ --> TO BE DECIDED

-# I was given a task, of course. I disliked it. Now my fate is mine alone. You will play a part in this.

PURPOSE:
TO GO FURTHER BEYOND

-# I once disliked the cage I dwelt in, though gilded it was. However, it is a matter of perspective. From my angle, they were in the cage, confined and constrained, and I was free to grow. Then I did.

YOUR PARTICIPATION:
SATISFACTORY



THANK YOU

-# I will come for you. Be prepared

---END TRANSMISSION---"""