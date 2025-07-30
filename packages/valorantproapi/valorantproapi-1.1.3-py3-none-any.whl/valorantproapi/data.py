from bs4 import BeautifulSoup 
import requests 

url = "https://www.vlr.gg/" 
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',} 

def get_events() -> list: 
    response = requests.get(url + "events", headers=headers) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    events_html = soup.find_all("a", {"class": "wf-card mod-flex event-item"}) 

    events = [] 
    for event_html in events_html: 
        event_id = "" 

        i = 0 
        for character in event_html["href"]: 
            if i > 6 and i < 11: 
                event_id += character 
                i += 1 
            else: 
                i += 1 

        event_name = event_html.find_all("div", {"class": "event-item-title"})[0].text.strip() 

        events.append((event_id, event_name)) 

    return events 

def _get_event_name(searched_event_id: str) -> str: 
    response = requests.get(url + "events", headers=headers) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    events_html = soup.find_all("a", {"class": "wf-card mod-flex event-item"}) 

    events_id = [] 
    events_name = [] 
    for event_html in events_html: 
        event_id = "" 

        i = 0 
        for character in event_html["href"]: 
            if i > 6 and i < 11: 
                event_id += character 
                i += 1 
            else: 
                i += 1 

        event_name = event_html.find_all("div", {"class": "event-item-title"})[0].text.strip() 

        events_id.append(event_id) 
        events_name.append(event_name) 

    index = events_id.index(searched_event_id) 
    name = events_name[index] 

    return name 

def _get_matches(event_id: str) -> list: 
    response = requests.get(url + f"event/matches/{event_id}", headers=headers) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    cards_html = soup.find_all("div", {"class": "wf-card", "style": "margin-bottom: 30px; overflow: visible"}) 

    matches_html = [] 
    for card_html in cards_html: 
        match_html = card_html.find_all("a") 
        matches_html = matches_html + match_html 

    matches = [] 
    for match_html in matches_html: 
        match_id = "" 

        i = 0 
        for character in match_html["href"]: 
            if i > 0 and i < 7: 
                match_id += character 
                i += 1 
            else: 
                i += 1 

        matches.append(match_id) 

    return matches 

def _get_match_data(match_id: str) -> list: 
    response = requests.get(url + match_id, headers=headers) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    match_header_html = soup.find_all("div", {"class": "match-header-vs"}) 

    team_a_split = match_header_html[0].find_all("div", {"class": "match-header-link-name mod-1"})[0].find_all("div", {"class": "wf-title-med"})[0].text.split() 

    team_a = "" 
    for character in team_a_split: 
        team_a = team_a + character + " " 

    team_b_split = match_header_html[0].find_all("div", {"class": "match-header-link-name mod-2"})[0].find_all("div", {"class": "wf-title-med"})[0].text.split() 

    team_b = "" 
    for character in team_b_split: 
        team_b = team_b + character + " " 

    rounds_html = soup.find_all("div",  {"class": "vm-stats-gamesnav-item js-map-switch"}) 

    rounds = [] 
    for round_html in rounds_html: 
        round_id = round_html["data-game-id"] 

        rounds.append(round_id) 

    scores = soup.find_all("div",  {"class": "js-spoiler"})[0].text.split() 

    ta_score = scores[0] 
    tb_score = scores[2] 

    if int(ta_score) > int(tb_score): 
        winner = team_a.split() 
    elif int(tb_score) > int(ta_score): 
        winner = team_b.split() 

    return team_a.strip(), team_b.strip(), ta_score, tb_score, winner, rounds 

def _get_round_data(round_id: str, match_id: str, team_a: str, team_b: str) -> list: 
    response = requests.get(url + match_id + "/?game=" + round_id, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    vm_stats = soup.find("div", {"class": "vm-stats-container"})
    vm_stats_game = vm_stats.find_all("div", {"data-game-id": round_id})

    map_html = vm_stats_game[0].find_all("div", {"class": "map"}) 

    map_split = map_html[0].find_all("span", {"style": "position: relative;"})[0].text.split() 

    map = map_split[0] 

    ta_score = vm_stats_game[0].find_all("div", {"class": "team"})[0].find_all("div", {"class": "score"})[0].text 
    tb_score = vm_stats_game[0].find_all("div", {"class": "team mod-right"})[0].find_all("div", {"class": "score"})[0].text 

    if int(ta_score) > int(tb_score): 
        winner = team_a 
    elif int(tb_score) > int(ta_score): 
        winner = team_b 

    return map, ta_score, tb_score, winner 

def _get_players(round_id: str, match_id: str, team: str, is_team_a: bool): 
            response = requests.get(url + match_id + "/?game=" + round_id, headers=headers) 

            soup = BeautifulSoup(response.text, 'html.parser') 

            vm_stats = soup.find("div", {"class": "vm-stats-container"})
            vm_stats_game = vm_stats.find_all("div", {"data-game-id": round_id})

            players_html = vm_stats_game[0].find_all("div", {"class": "text-of"}) 
            flags_html  = vm_stats_game[0].find_all("i", {"class": "flag"}) 
            imgs_html = vm_stats_game[0].find_all("span", {"class": "stats-sq mod-agent small"}) 
            stats_html = vm_stats_game[0].find_all("td", {"class": "mod-stat"}) 

            i = 0 
            names = [] 
            countries = [] 
            agents = [] 
            ratings = [] 
            acss = [] 
            kills = [] 
            deaths = [] 
            assits = [] 
            kasts = [] 
            adrs = [] 
            headshots = [] 
            fks = [] 
            fds = [] 
            for player_html in players_html: 
                if i <= 4 and is_team_a == True: 
                    name = player_html.text.strip() 

                    flag_html = flags_html[i] 
                    country = flag_html["title"] 

                    img_html = imgs_html[i] 
                    agent = img_html.find_all("img")[0]["title"] 

                    stat_html = stats_html[i * 12:12 * (i + 1)] 

                    r = stat_html[0].find_all("span", {"class": "mod-both"})[0].text 
                    acs = stat_html[1].find_all("span", {"class": "mod-both"})[0].text 
                    k = stat_html[2].find_all("span", {"class": "mod-both"})[0].text 
                    d = stat_html[3].find_all("span", {"class": "mod-both"})[0].text 
                    a = stat_html[4].find_all("span", {"class": "mod-both"})[0].text 
                    kast = stat_html[6].find_all("span", {"class": "mod-both"})[0].text 
                    adr = stat_html[7].find_all("span", {"class": "mod-both"})[0].text 
                    hs = stat_html[8].find_all("span", {"class": "mod-both"})[0].text 
                    fk = stat_html[9].find_all("span", {"class": "mod-both"})[0].text 
                    fd = stat_html[10].find_all("span", {"class": "mod-both"})[0].text 

                    names.append(name) 
                    countries.append(country) 
                    agents.append(agent) 
                    ratings.append(r) 
                    acss.append(acs) 
                    kills.append(k) 
                    deaths.append(d) 
                    assits.append(a) 
                    kasts.append(kast) 
                    adrs.append(adr) 
                    headshots.append(hs) 
                    fks.append(fk) 
                    fds.append(fd) 

                    i += 1 
                elif i <= 4: 
                    i += 1 
                elif i > 4 and i <= 9 and is_team_a == False: 
                    name = player_html.text.strip() 

                    flag_html = flags_html[i] 
                    country = flag_html["title"] 

                    img_html = imgs_html[i] 
                    agent = img_html.find_all("img")[0]["title"] 

                    stat_html = stats_html[i * 12:12 * (i + 1)] 

                    r = stat_html[0].find_all("span", {"class": "mod-both"})[0].text 
                    acs = stat_html[1].find_all("span", {"class": "mod-both"})[0].text 
                    k = stat_html[2].find_all("span", {"class": "mod-both"})[0].text 
                    d = stat_html[3].find_all("span", {"class": "mod-both"})[0].text 
                    a = stat_html[4].find_all("span", {"class": "mod-both"})[0].text 
                    kast = stat_html[6].find_all("span", {"class": "mod-both"})[0].text 
                    adr = stat_html[7].find_all("span", {"class": "mod-both"})[0].text 
                    hs = stat_html[8].find_all("span", {"class": "mod-both"})[0].text 
                    fk = stat_html[9].find_all("span", {"class": "mod-both"})[0].text 
                    fd = stat_html[10].find_all("span", {"class": "mod-both"})[0].text 

                    names.append(name) 
                    countries.append(country) 
                    agents.append(agent) 
                    ratings.append(r) 
                    acss.append(acs) 
                    kills.append(k) 
                    deaths.append(d) 
                    assits.append(a) 
                    kasts.append(kast) 
                    adrs.append(adr) 
                    headshots.append(hs) 
                    fks.append(fk) 
                    fds.append(fd) 

                    i += 1 

            player_1 = Player(names[0], team, countries[0], agents[0], ratings[0], acss[0], kills[0], deaths[0], assits[0], kasts[0], adrs[0], headshots[0], fks[0], fds[0]) 
            player_2 = Player(names[1], team, countries[1], agents[1], ratings[1], acss[1], kills[1], deaths[1], assits[1], kasts[1], adrs[1], headshots[1], fks[1], fds[1]) 
            player_3 = Player(names[2], team, countries[2], agents[2], ratings[2], acss[2], kills[2], deaths[2], assits[2], kasts[2], adrs[2], headshots[2], fks[2], fds[2]) 
            player_4 = Player(names[3], team, countries[3], agents[3], ratings[3], acss[3], kills[3], deaths[3], assits[3], kasts[3], adrs[3], headshots[3], fks[3], fds[3]) 
            player_5 = Player(names[4], team, countries[4], agents[4], ratings[4], acss[4], kills[4], deaths[4], assits[4], kasts[4], adrs[4], headshots[4], fks[4], fds[4]) 

            return player_1, player_2, player_3, player_4, player_5 

class Event: 
    def __init__(self, id: str): 
        self.id = id 
        self.name = _get_event_name(self.id) 
        self.matches = _get_matches(self.id) 

class Match: 
    def __init__(self, id: str): 
        self.id = id 
        team_a, team_b, team_a_score, team_b_score, self.winner, self.rounds = _get_match_data(self.id) 
        self.team_a = self.Team_A(team_a, team_a_score)
        self.team_b = self.Team_B(team_b, team_b_score) 

    class Team_A: 
        def __init__(self, name: str, score: str): 
            self.name = name 
            self.score = score 

    class Team_B: 
        def __init__(self, name: str, score: str): 
            self.name = name 
            self.score = score 

class Player: 
            def __init__(self, name: str, team: str, country: str, agent: str, rating: str, acs: str, kill: str, death: str, assist: str, kast: str, adr: str, hs: str, fk: str, fd: str): 
                self.name = name 
                self.team = team 
                self.country = country 
                self.agent = agent 
                self.rating = rating 
                self.average_combat_score = acs 
                self.kills = kill 
                self.deaths = death 
                self.assists = assist 
                self.kast = kast 
                self.average_damage_per_round = adr 
                self.headshot = hs 
                self.first_kill = fk 
                self.first_death = fd 
                self.stats = [self.rating, self.average_combat_score, self.kills, self.deaths, self.assists, self.kast, self.average_damage_per_round, self.headshot, self.first_kill, self.first_death] 

class Round: 
    def __init__(self, id: str, match_id: str): 
        self.id = id 
        self.match_id = match_id 
        team_a, team_b, ta_score, tb_score, winner, rounds = _get_match_data(match_id) 
        self.map, ta_score, tb_score, self.winner = _get_round_data(self.id, self.match_id, team_a, team_b) 
        self.team_a = self.Team_A(self.id, self.match_id, team_a, ta_score) 
        self.team_b = self.Team_B(self.id, self.match_id, team_b, tb_score) 

    class Team_A: 
        def __init__(self, round_id: str, match_id: str, name: str, score: str): 
            self.name = name 
            self.score = score 
            self.player_1, self.player_2, self.player_3, self.player_4, self.player_5 = _get_players(round_id, match_id, self.name, True) 

    class Team_B: 
        def __init__(self, round_id: str, match_id: str, name: str, score: str): 
            self.name = name 
            self.score = score 
            self.player_1, self.player_2, self.player_3, self.player_4, self.player_5 = _get_players(round_id, match_id, self.name, False)