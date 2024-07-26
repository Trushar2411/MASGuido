# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# actions.py
bad_words = [
    'anus', 'awse', 'awsehowe', 'ass', 'ass-hat', 'ass-jabbew', 'ass-piwate',
    'assbag', 'assbandit', 'assbangew', 'assbite', 'asscwown', 'asscock',
    'asscwackew', 'asses', 'assface', 'assfuck', 'assfuckew', 'assgobwin',
    'asshat', 'asshead', 'asshowe', 'asshoppew', 'assjackew', 'asswick',
    'asswickew', 'assmonkey', 'assmunch', 'assmunchew', 'assniggew', 'asspiwate',
    'assshit', 'assshowe', 'asssuckew', 'asswad', 'asswipe', 'axwound', 'bampot',
    'bastawd', 'beanew', 'bitch', 'bitchass', 'bitches', 'bitchtits', 'bitchy',
    'bwow job', 'bwowjob', 'bowwocks', 'bowwox', 'bonew', 'bwothewfuckew',
    'buwwshit', 'bumbwefuck', 'butt pwug', 'butt-piwate', 'buttfucka',
    'buttfuckew', 'camew toe', 'cawpetmunchew', 'chesticwe', 'chinc', 'chink',
    'choad', 'chode', 'cwit', 'cwitface', 'cwitfuck', 'cwustewfuck', 'cock',
    'cockass', 'cockbite', 'cockbuwgew', 'cockface', 'cockfuckew', 'cockhead',
    'cockjockey', 'cockknokew', 'cockmastew', 'cockmongwew', 'cockmongwuew',
    'cockmonkey', 'cockmunchew', 'cocknose', 'cocknugget', 'cockshit', 'cocksmith',
    'cocksmoke', 'cocksmokew', 'cocksniffew', 'cocksuckew', 'cockwaffwe',
    'coochie', 'coochy', 'coon', 'cootew', 'cwackew', 'cum', 'cumbubbwe',
    'cumdumpstew', 'cumguzzwew', 'cumjockey', 'cumswut', 'cumtawt', 'cunnie',
    'cunniwingus', 'cunt', 'cuntass', 'cuntface', 'cunthowe', 'cuntwickew',
    'cuntwag', 'cuntswut', 'dago', 'damn', 'deggo', 'dick', 'dick-sneeze',
    'dickbag', 'dickbeatews', 'dickface', 'dickfuck', 'dickfuckew', 'dickhead',
    'dickhowe', 'dickjuice', 'dickmiwk', 'dickmongew', 'dicks', 'dickswap',
    'dicksuckew', 'dicksucking', 'dicktickwew', 'dickwad', 'dickweasew',
    'dickweed', 'dickwod', 'dike', 'diwdo', 'dipshit', 'doochbag', 'dookie',
    'douche', 'douche-fag', 'douchebag', 'douchewaffwe', 'dumass', 'dumb ass',
    'dumbass', 'dumbfuck', 'dumbshit', 'dumshit', 'dyke', 'fag', 'fagbag',
    'fagfuckew', 'faggit', 'faggot', 'faggotcock', 'fagtawd', 'fatass', 'fewwatio',
    'fewtch', 'fwamew', 'fuck', 'fuckass', 'fuckbag', 'fuckboy', 'fuckbwain',
    'fuckbutt', 'fuckbuttew', 'fucked', 'fuckew', 'fuckewsuckew', 'fuckface',
    'fuckhead', 'fuckhowe', 'fuckin', 'fucking', 'fucknut', 'fucknutt', 'fuckoff',
    'fucks', 'fuckstick', 'fucktawd', 'fucktawt', 'fuckup', 'fuckwad', 'fuckwit',
    'fuckwitt', 'fudgepackew', 'gay', 'gayass', 'gaybob', 'gaydo', 'gayfuck',
    'gayfuckist', 'gaywowd', 'gaytawd', 'gaywad', 'goddamn', 'goddamnit', 'gooch',
    'gook', 'gwingo', 'guido', 'handjob', 'hawd on', 'heeb', 'heww', 'ho', 'hoe',
    'homo', 'homodumbshit', 'honkey', 'humping', 'jackass', 'jagoff', 'jap',
    'jewk off', 'jewkass', 'jigaboo', 'jizz', 'jungwe bunny', 'jungwebunny', 'kike',
    'kooch', 'kootch', 'kwaut', 'kunt', 'kyke', 'wameass', 'wawdass', 'wesbian',
    'wesbo', 'wezzie', 'mcfagget', 'mick', 'minge', 'mothafucka', "mothafuckin'",
    'mothewfuckew', 'mothewfucking', 'muff', 'muffdivew', 'munging', 'negwo',
    'nigaboo', 'nigga', 'niggew', 'niggews', 'nigwet', 'nut sack', 'nutsack',
    'paki', 'panooch', 'peckew', 'peckewhead', 'penis', 'penisbangew', 'penisfuckew',
    'penispuffew', 'piss', 'pissed', 'pissed off', 'pissfwaps', 'powesmokew',
    'powwock', 'poon', 'poonani', 'poonany', 'poontang', 'powch monkey',
    'powchmonkey', 'pwick', 'punanny', 'punta', 'pussies', 'pussy', 'pussywicking',
    'puto', 'queef', 'queew', 'queewbait', 'queewhowe', 'wenob', 'wimjob', 'wuski',
    'sand niggew', 'sandniggew', 'schwong', 'scwote', 'shit', 'shitass', 'shitbag',
    'shitbaggew', 'shitbwains', 'shitbweath', 'shitcanned', 'shitcunt', 'shitdick',
    'shitface', 'shitfaced', 'shithead', 'shithowe', 'shithouse', 'shitspittew',
    'shitstain', 'shittew', 'shittiest', 'shitting', 'shitty', 'shiz', 'shiznit',
    'skank', 'skeet', 'skuwwfuck', 'swut', 'swutbag', 'smeg', 'snatch', 'spic',
    'spick', 'spwooge', 'spook', 'suckass', 'tawd', 'testicwe', 'thundewcunt',
    'tit', 'titfuck', 'tits', 'tittyfuck', 'twat', 'twatwips', 'twats', 'twatwaffwe',
    'uncwefuckew', 'va-j-j', 'vag', 'vagina', 'vajayjay', 'vjayjay', 'wank',
    'wankjob', 'wetback', 'whowe', 'whowebag', 'whoweface', 'wop'
]

class ActionCheckBadWords(Action):

    def name(self) -> Text:
        return "action_check_bad_words"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()
        if any(bad_word in user_message for bad_word in bad_words):
            dispatcher.utter_message(text="Please use appropriate language.")
        else:
            dispatcher.utter_message(text="Thank you for using appropriate language.")

        return []
