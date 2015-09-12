import requests
import json
import re

class Game:
    def __init__(self, game_url='http://data.ncaa.com/jsonp/game/football/fbs/2015/09/03/michigan-utah/pbp.json?callback=ncaaGameTabs.drawTab'):
        self.session = requests.Session()

        r = self.session.get(game_url)

        cleaned_response_text = self.clean_text_response(r.text)
        pbp_json = json.loads(cleaned_response_text)

        self.plays_json = pbp_json['periods']

        meta = pbp_json['meta']
        self.home_team = self.get_home_team(meta)
        self.away_team = self.get_away_team(meta)

    def clean_text_response(self, response_text):
        response_text = response_text.replace('ncaaGameTabs.drawTab(', '')
        response_text = response_text[0:len(response_text) - 2]
        return response_text

    def get_home_team(self, meta_data):
        home_team_name = meta_data['teams'][1]['shortname']
        home_team_id = meta_data['teams'][1]['id']
        return Team(self.plays_json, home_team_name, home_team_id)

    def get_away_team(self, meta_data):
        away_team_name = meta_data['teams'][0]['shortname']
        away_team_id = meta_data['teams'][0]['id']
        return Team(self.plays_json, away_team_name, away_team_id)

class Team:    
    def __init__(self, play_by_play_json, team_name, team_id):
        self.possessions = []
        self.play_by_play_json = play_by_play_json
        self.team_name = team_name
        self.team_id = team_id
        self.get_plays()

    def get_plays(self):
        for period in self.play_by_play_json:
            all_possessions = period['possessions']
            for possession in all_possessions:
                if possession['teamId'] == self.team_id:
                    self.possessions.append(Possession(possession['plays'], self.team_id))
        print(self.team_name + ' has ' + str(len(self.possessions)) + ' possessions.')

class Possession:
    def __init__(self, plays, team_id):
        self.plays = []
        self.team_id = team_id
        for play_json in plays:
            play = Play(play_json['driveText'], play_json['scoreText'])
            if self.is_valid_play(play.play_description):
                self.plays.append(play)

    def is_valid_play(self, play_description):
        invalid_words = ['kicks', 'kneels', 'extra point']
        for word in invalid_words:
            if word in play_description:
                return False
        return True

class Play:
    def __init__(self, down_and_distance_los, play_description):
        self.play_description = play_description

        self.down = self.set_down(down_and_distance_los)
        self.distance_to_go = self.set_distance_to_go(down_and_distance_los)
        self.line_of_scrimmage = self.set_line_of_scrimmage(down_and_distance_los)

    def set_down(self, down_and_distance_los):
        if down_and_distance_los != None and down_and_distance_los != '':
            return int(down_and_distance_los[0:1])

    def set_distance_to_go(self, down_and_distance_los):
        if down_and_distance_los != None and down_and_distance_los != '':
            numbers = re.findall(r'\d+', down_and_distance_los)
            if len(numbers) > 1:
                print(numbers[1])
                return int(numbers[1])

    def set_line_of_scrimmage(self, down_and_distance_los):
        return 20

g = Game()


