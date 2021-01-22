def _get_riot_api_data():

    riot_game_data = dict()

    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        game_data = requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify=False)
    except Exception as err:
        print(str(err))
        return dict()
    game_data = game_data.json()

    character_stats = dict()
    character_stats["eLevel"] = game_data["activePlayer"]["abilities"]["E"]["abilityLevel"]
    character_stats["qLevel"] = game_data["activePlayer"]["abilities"]["Q"]["abilityLevel"]
    character_stats["rLevel"] = game_data["activePlayer"]["abilities"]["R"]["abilityLevel"]
    character_stats["wLevel"] = game_data["activePlayer"]["abilities"]["W"]["abilityLevel"]

    character_stats.update(game_data["activePlayer"]["championStats"])
    character_stats["currentGold"] = game_data["activePlayer"]["currentGold"]
    character_stats["summonerName"] = game_data["activePlayer"]["summonerName"]

    riot_game_data["allPlayers"] = []

    for player in game_data["allPlayers"]:
        player_stats = dict()
        player_stats["championName"] = player["championName"]
        player_stats["summonerName"] = player["summonerName"]
        player_stats["items"] = player["items"]
        player_stats["level"] = player["level"]
        player_stats["respawnTimer"] = player["respawnTimer"]
        player_stats["creepScore"] = player["scores"]["creepScore"]
        player_stats["kills"] = player["scores"]["kills"]
        player_stats["assists"] = player["scores"]["assists"]
        player_stats["deaths"] = player["scores"]["deaths"]
        player_stats["team"] = player["team"]

        if player["summonerName"] == character_stats["summonerName"]:
            character_stats.update(player_stats)
        else:
            riot_game_data["allPlayers"].append(player_stats)

    riot_game_data["characterStats"] = character_stats
    riot_game_data["gameTime"] = game_data["gameData"]["gameTime"]

    return riot_game_data