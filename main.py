from bs4 import BeautifulSoup, Doctype
import urllib.request
import re

# Some coding guidance taken from https://nullprogram.com/blog/2017/05/15/
    # And BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Create a skeleton HTML doc
doc = BeautifulSoup(features='html.parser')
doc.append(Doctype('html'))

# Flesh out the skeleton a bit
html = doc.new_tag('html', lang='en-US')
doc.append(html)
head = doc.new_tag('head')
html.append(head)
meta = doc.new_tag('meta', charset='utf-8')
head.append(meta)
title = doc.new_tag('title')
title.string = 'The Deathworlders'
head.append(title)
body = doc.new_tag('body')
html.append(body)

# Make a list of all the chapter URLs, in order
chapters = [
    "https://deathworlders.com/books/deathworlders/chapter-00-kevin-jenkins-experience/",
    "https://deathworlders.com/books/deathworlders/chapter-01-run-little-monster/",
    "https://deathworlders.com/books/deathworlders/chapter-02-aftermath/",
    "https://deathworlders.com/books/deathworlders/chapter-03-eventful-month/",
    "https://deathworlders.com/books/deathworlders/chapter-04-quarantine/",
    "https://deathworlders.com/books/deathworlders/chapter-05-deliverance/",
    "https://deathworlders.com/books/deathworlders/chapter-05.5-interlude-ultimatum/",
    "https://deathworlders.com/books/deathworlders/chapter-06-taking-back-sky/",
    "https://deathworlders.com/books/deathworlders/chapter-06.5-interlude-jargon/",
    "https://deathworlders.com/books/deathworlders/chapter-07-tensions/",
    "https://deathworlders.com/books/deathworlders/chapter-08-alternatives/",
    "https://deathworlders.com/books/deathworlders/chapter-09-gains-losses/",
    "https://deathworlders.com/books/deathworlders/chapter-10-legwork/",
    "https://deathworlders.com/books/deathworlders/chapter-11-direct-delivery/",
    "https://deathworlders.com/books/deathworlders/chapter-12-only-human/",
    "https://deathworlders.com/books/deathworlders/chapter-13-tall-tales/",
    "https://deathworlders.com/books/deathworlders/chapter-14-hornets-nest/",
    "https://deathworlders.com/books/deathworlders/chapter-15-forever-changed/",
    "https://deathworlders.com/books/deathworlders/chapter-16-firebird/",
    "https://deathworlders.com/books/deathworlders/chapter-17-battles/",
    "https://deathworlders.com/books/deathworlders/chapter-18-baggage/",
    "https://deathworlders.com/books/deathworlders/chapter-19-baptisms/",
    "https://deathworlders.com/books/deathworlders/chapter-20-exorcisms/",
    "https://deathworlders.com/books/deathworlders/chapter-21-dragon-dreams/",
    "https://deathworlders.com/books/deathworlders/chapter-21.5-interlude-d4-d5-c4-dxc4/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt1-first-year/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt2-second-year/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt3-third-year/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt4-fourth-year/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt5-fifth-year/",
    "https://deathworlders.com/books/deathworlders/chapter-22-warhorse-pt6-operation-nova-hound/",
    "https://deathworlders.com/books/deathworlders/chapter-22.5-interlude-outlets/",
    "https://deathworlders.com/books/deathworlders/chapter-23-back-down-earth/",
    "https://deathworlders.com/books/deathworlders/chapter-24-alien-world/",
    "https://deathworlders.com/books/deathworlders/chapter-25-where-we-stand/",
    "https://deathworlders.com/books/good-training/1-fun-games/",
    "https://deathworlders.com/books/good-training/2-strategies/",
    "https://deathworlders.com/books/good-training/3-instinct/",
    "https://deathworlders.com/books/good-training/4-crawl/",
    "https://deathworlders.com/books/good-training/5-walk/",
    "https://deathworlders.com/books/good-training/6-friendships-revelations/",
    "https://deathworlders.com/books/good-training/7-run/",
    "https://deathworlders.com/books/good-training/8-fetch/",
    "https://deathworlders.com/books/good-training/9-aftermath/",
    "https://deathworlders.com/books/good-training/10-essayons/",
    "https://deathworlders.com/books/good-training/11-shenanigans/",
    "https://deathworlders.com/books/good-training/12-wargames/",
    "https://deathworlders.com/books/good-training/13-adventure-time/",
    "https://deathworlders.com/books/deathworlders/chapter-26-blood-ash/",
    "https://deathworlders.com/books/deathworlders/chapter-27-playing-fire/",
    "https://deathworlders.com/books/deathworlders/chapter-28-misfits/",
    "https://deathworlders.com/books/deathworlders/chapter-29-forges/",
    "https://deathworlders.com/books/good-training-champions-pt-i/1-prologue/",
    "https://deathworlders.com/books/good-training-champions-pt-i/2-tooth-claw/",
    "https://deathworlders.com/books/good-training-champions-pt-i/3-longest-prefix-match/",
    "https://deathworlders.com/books/good-training-champions-pt-i/4-gametime/",
    "https://deathworlders.com/books/deathworlders/chapter-30-hearts-minds/",
    "https://deathworlders.com/books/deathworlders/chapter-31-touching-down/",
    "https://deathworlders.com/books/deathworlders/chapter-32-deep-wounds/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/1-pounce/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/2-kin-clan/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/3-tall-tales/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/4-first-ring/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/5-plans-plots/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/6-beginnings-endings/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/7-doom-gloom/",
    "https://deathworlders.com/books/good-training-champions-pt-ii/8-tidying-up/",
    "https://deathworlders.com/books/deathworlders/chapter-33-metadyskolia/",
    "https://deathworlders.com/books/deathworlders/chapter-34-states-mind/",
    "https://deathworlders.com/books/deathworlders/chapter-35-event-horizions/",
    "https://deathworlders.com/books/deathworlders/chapter-36-consequences/",
    "https://deathworlders.com/books/deathworlders/chapter-37-grounded/",
    "https://deathworlders.com/books/deathworlders/chapter-38-paroxysm/",
    "https://deathworlders.com/books/deathworlders/chapter-39-nirvana-cage/",
    "https://deathworlders.com/books/deathworlders/chapter-40-war-two-worlds-pt1-instigation/",
    "https://deathworlders.com/books/deathworlders/chapter-40-war-two-worlds-pt2-escalation/",
    "https://deathworlders.com/books/deathworlders/chapter-40-war-two-worlds-pt3-consolidation/",
    "https://deathworlders.com/books/deathworlders/chapter-40-war-two-worlds-pt4-retaliation/",
    "https://deathworlders.com/books/deathworlders/chapter-40-war-two-worlds-pt5-cremation/",
    "https://deathworlders.com/books/good-training/survival/",
    "https://deathworlders.com/books/waters-babylon/1-tzedakah/",
    "https://deathworlders.com/books/deathworlders/chapter-41-pyrophytes/",
    "https://deathworlders.com/books/waters-babylon/2-tikkun-olam/",
    "https://deathworlders.com/books/waters-babylon/3-mitzvah/",
    "https://deathworlders.com/books/deathworlders/chapter-42-big-questions/",
    "https://deathworlders.com/books/deathworlders/chapter-43-scars-both-old-new/",
    "https://deathworlders.com/books/deathworlders/chapter-44-samsara/",
    "https://deathworlders.com/books/deathworlders/chapter-45-we-need-each-other/",
    "https://deathworlders.com/books/bolthole-aces/chapter-00-prelude-to-war/",
    "https://deathworlders.com/books/deathworlders/chapter-46-hellfall/",
    "https://deathworlders.com/books/bolthole-aces/chapter-01-innocence-lost/",
    "https://deathworlders.com/books/deathworlders/chapter-47-fallout/",
    "https://deathworlders.com/books/deathworlders/chapter-48-laid-bare/",
    "https://deathworlders.com/books/deathworlders/chapter-49-division/",
    "https://deathworlders.com/books/deathworlders/chapter-50-counterattack-pt1-regroup/",
    "https://deathworlders.com/books/deathworlders/chapter-50-counterattack-pt2-homefront/",
    "https://deathworlders.com/books/deathworlders/chapter-50-counterattack-pt3-trigger/",
    "https://deathworlders.com/books/deathworlders/chapter-51-anticlimax/",
    "https://deathworlders.com/books/deathworlders/chapter-52-autoimmune/",
    "https://deathworlders.com/books/deathworlders/chapter-53-the-wild-hunt/",
    "https://deathworlders.com/books/deathworlders/chapter-54-here-be-dragons/",
    "https://deathworlders.com/books/deathworlders/chapter-55-reinvention/",
    "https://deathworlders.com/books/deathworlders/chapter-56-dataquake/",
    "https://deathworlders.com/books/deathworlders/chapter-57-cat-and-mouse-pt1-hunter-and-hunted/",
    "https://deathworlders.com/books/deathworlders/chapter-57-cat-and-mouse-pt2-worlds-in-the-dark/",
    "https://deathworlders.com/books/deathworlders/chapter-58-gjallarhorn/",
    "https://deathworlders.com/books/deathworlders/chapter-59-new-life/",
    "https://deathworlders.com/books/deathworlders/chapter-60-the-calm-and-the-storm/",
    "https://deathworlders.com/books/deathworlders/chapter-61-violence/",
    "https://deathworlders.com/books/deathworlders/chapter-62-tooth-and-claw/",
    "https://deathworlders.com/books/deathworlders/chapter-63-torn/",
    "https://deathworlders.com/books/deathworlders/chapter-64-survive/",
    "https://deathworlders.com/books/deathworlders/chapter-65-leaps-of-faith/",
    "https://deathworlders.com/books/deathworlders/chapter-66-unbowed/",
    "https://deathworlders.com/books/deathworlders/chapter-67-resurgence/",
    "https://deathworlders.com/books/deathworlders/chapter-68-nadir/",
    "https://deathworlders.com/books/deathworlders/chapter-69-lockdown/",
    "https://deathworlders.com/books/deathworlders/chapter-70-death-eye-pt1/"
]

# Test on one chapter
# Grab the title
url_open = urllib.request.urlopen(chapters[2])
page = BeautifulSoup(url_open, features='html.parser')
    # Inside out:
        # page select grabs the h1 element under main
        # regex to take what is in between > <
# title = re.findall(r'>(.*?)<' ,str(page.select('main h1')[0]))[0]
title = page.find_all('h1')
title = title[1].text
# Grab the content
content = [x.text for x in page.select('article p')]


# Do it on all the chapters and put it in the output document
for chapter in chapters:
    url_open = urllib.request.urlopen(chapter)
    page = BeautifulSoup(url_open, features='html.parser')

    title = page.find_all('h1')
    title = title[1].text
    header = doc.new_tag('h1')
    header.string = title
    body.append(header)

    content = [x.text for x in page.select('article p')]
    for i, p in enumerate(content):
        body.append(doc.new_tag('p'))
        # I was using regex to filter out the text but opted for bs4's .text instead
            # This try/except was to see why the errors were occuring but couldn't figure it out
                # bs4 .text seemingly solves the problem 
        try:
            body.append(p)
        except:
            print(f"Chapter title: {title}\nP number: {i}")

# Write it to an html file in the folder
with open("Deathworlders_Output.html", "w", encoding='utf-8') as file:
    file.write(str(doc))

