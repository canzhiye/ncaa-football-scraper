import game

def is_valid_play(play_description):
    if ('kicks' in play_description) or ('kneels' in play_description):
        return False
    else:
        return True

def calculate_success_rate(team):
    total_plays = 0
    successful_plays = 0

    for possession in team.possessions:
        # print(team.team_id)
        # print(possession.team_id)
        # print('\n')

        # might be redundant
        while (len(possession.plays) > 0) and (not is_valid_play(possession.plays[0].play_description)):
            possession.plays.pop(0)

        if len(possession.plays) < 1:
            break

        previous_play = possession.plays[0]
        possession.plays.pop(0)

        for play in possession.plays:
            total_plays += 1

            print('it was ' + str(previous_play.down))
            print('now it is ' + str(play.down))
            print(previous_play.play_description)
            print(play.play_description)

            if play.down <= previous_play.down:
                # first down!
                print('first down!')
                successful_plays += 1
            else:
                # calculate
                print('next down')
                if play.down == 2:
                    yards_gained = previous_play.distance_to_go - play.distance_to_go
                    print(str(yards_gained) + ' yards were gained on 1st down.')

                    if yards_gained > 0.5 * previous_play.distance_to_go:
                        successful_plays += 1
                elif play.down == 3:
                    yards_gained = previous_play.distance_to_go - play.distance_to_go
                    if yards_gained > 0.7 * previous_play.distance_to_go:
                        successful_plays += 1
            print('\n')

            previous_play = play

    return successful_plays / total_plays

home_success_rate = calculate_success_rate(game.g.home_team)
print(home_success_rate)

away_success_rate = calculate_success_rate(game.g.away_team)
print(away_success_rate)


