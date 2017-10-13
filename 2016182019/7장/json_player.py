import main_state
import json
def create_team():
    player_state_table = {
        "LEFT_RUN" : main_state.Boy.LEFT_RUN,
        "RIGHT_RUN": main_state.Boy.RIGHT_RUN,
        "LEFT_STAND": main_state.Boy.LEFT_STAND,
        "RIGHT_STAND": main_state.Boy.RIGHT_STAND
    }
    team_data_file = open('team_data.json')
    team_data = json.load(team_data_file)
    team_data_file.close()
    team = []
    for name in team_data:
        player = main_state.Boy()
        player.name = name
        player.x = team_data[name]['x']
        player.y = team_data[name]['y']
        player.state = player_state_table[team_data[name]['StartState']]
        team.append(player)
    return team
