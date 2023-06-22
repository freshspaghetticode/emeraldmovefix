# scraper.py

# The developer of this project would like to credit
# the poor souls at Bulbagarden and Serebii
# who did the hard work of compiling these learnsets
# into articles accessible through Python.
# Your work does not go unappreciated.

import os
import urllib.request
from move import Move
from pokemon import Pokemon

src = os.getcwd()
scrape = os.getcwd() + "\scrape"

def main():    
    print("This is a test!")
    pokemon_list = populate_hoenn_pokedex()
    #scrape_pages(pokemon_list)
    pokemon_list = populate_moves(pokemon_list)
    deoxys = Pokemon()
    deoxys.name = "Deoxys"
    deoxys.pokedex_number = 386
    deoxys.url = "https://bulbapedia.bulbagarden.net/wiki/Deoxys_(Pok%C3%A9mon)/Generation_III_learnset"
    deoxys = populate_deoxys_speed(deoxys)
    pokemon_list.append(deoxys)
    for pokemon in pokemon_list:
        if "Mew" in pokemon.name:
            for move in pokemon.emerald_tutor_moves:
                print(move.name)


def populate_hoenn_pokedex():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_Hoenn_Pok%C3%A9dex_number_(Generation_III)"
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    
    html_source = response.read()

    with open("temp_stored_page.txt", "wb") as temp_stored_page_write:
        temp_stored_page_write.write(html_source)
    print("page saved.")

    output_pokemon_list = []
    i = 0
    # make 385 Pokemon, Deoxys is a special case that will be appended to the end
    while i < 385:
        new_pokemon = Pokemon()
        output_pokemon_list.append(new_pokemon)
        print("made new pokemon! continuing...")
        i += 1

    print("empty pokedex made.")

    name = ""
    pokedex_number = -1
    url = ""

    name_found = False
    pokedex_number_found = False

    flag = False

    temp_stored_page_read = open("temp_stored_page.txt", "r", encoding="utf8")

    for line in temp_stored_page_read:
                # this line of HTML contains the pokedex number
                if 'style="font-family:monospace">#' in line:
                    # we want to take the second number, which is the national dex number
                    if(flag):
                        pokedex_number = int(line[line.find('#')+1:len(line)])
                        pokedex_number_found = True
                        flag = False
                    else:
                        flag = True
                # this line contains the name and url of the wiki page for the pokemon
                elif '_(Pok%C3%A9mon)' in line and 'Pokémon' in line:
                    name = line[line.find(')">')+3:line.find('</a>')]
                    url = "https://bulbapedia.bulbagarden.net/wiki/" + line[line.find('/wiki/')+6:line.find('_(Pok')] + "_(Pok%C3%A9mon)/Generation_III_learnset"
                    name_found = True

                if name == "Deoxys":
                    continue

                if name_found and pokedex_number_found:
                    output_pokemon_list[pokedex_number - 1].name = name
                    output_pokemon_list[pokedex_number - 1].pokedex_number = pokedex_number
                    output_pokemon_list[pokedex_number - 1].url = url
                    name_found = False
                    pokedex_number_found = False
                    print("updated pokemon! continuing...")

    return output_pokemon_list

def populate_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    output_pokemon_list = populate_level_up_moves(output_pokemon_list)
    output_pokemon_list = populate_tm_moves(output_pokemon_list)
    output_pokemon_list = populate_egg_moves(output_pokemon_list)
    output_pokemon_list = populate_tutor_moves(output_pokemon_list)
    output_pokemon_list = populate_purified_moves(output_pokemon_list)
    output_pokemon_list = populate_prior_moves(output_pokemon_list)
    output_pokemon_list = populate_event_moves(output_pokemon_list)
    return output_pokemon_list

def scrape_pages(input_pokemon_list):
    
    # change directory for task
    os.chdir(scrape)

    for pokemon in input_pokemon_list:
        print(pokemon.name)

        # start session
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        url = pokemon.url
        headers={'User-Agent':user_agent,} 
        request=urllib.request.Request(url,None,headers) #The assembled request
        response = urllib.request.urlopen(request)
        
        html_source = response.read()

        # save html source
        with open(str(pokemon.pokedex_number) + ".txt", "wb") as temp_stored_page_write:
            temp_stored_page_write.write(html_source)
        print(pokemon.name + ": page saved.")

    # revert directory to default
    os.chdir(src)

    return

def populate_event_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading event moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = 'title="Event'
        found_start_keyword = False

        found_move = False

        name = ""

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for moves in line
            if "_(move)" in line:
                found_move = True
                name = line[line.find('title="')+7:line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                pokemon.event_moves.append(Move(name))

    # revert directory to default
    os.chdir(src)

    print("event moves finished.")
    return output_pokemon_list

def populate_prior_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading prior evolution moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "By_a_prior_evolution"
        found_start_keyword = False

        found_move = False

        name = ""

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for moves in line
            if "_(move)" in line:
                found_move = True
                name = line[line.find('title="')+7:line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                pokemon.prior_moves.append(Move(name))

    # revert directory to default
    os.chdir(src)

    print("prior evolution moves finished.")
    return output_pokemon_list

def populate_purified_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading purified moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "Special_moves"
        found_start_keyword = False

        found_move = False

        name = ""

        temp_line = ""
        special_counter = -3
        counter = 0
        mass_outbreak_flag = False

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for moves in line
            if "Mass outbreak" in line:
                mass_outbreak_flag = True
            if "_(move)" in line:
                special_counter = counter
                temp_line = line
            elif "_(type)" in line and special_counter + 2 == counter:
                found_move = True
                special_counter = -3
                name = temp_line[temp_line.find('title="')+7:temp_line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                if mass_outbreak_flag:
                    mass_outbreak_flag = False
                    pokemon.mass_outbreak_moves.append(Move(name))
                else:
                    pokemon.purified_moves.append(Move(name))
            
            counter = counter + 1

    # revert directory to default
    os.chdir(src)

    print("purified moves finished.")
    return output_pokemon_list

def populate_tutor_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading tutor moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "By_tutoring"
        found_start_keyword = False

        found_move = False

        name = ""

        emerald_tutor_flag = False
        firered_tutor_flag = False
        xd_tutor_flag = False

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # check tutor status
            if "LeafGreen Versions" in line:
                firered_tutor_flag = True
            if "Emerald Version" in line:
                emerald_tutor_flag = True
            if "Gale of Darkness" in line:
                xd_tutor_flag = True

            # search for moves in line
            if "_(move)" in line:
                found_move = True
                name = line[line.find('title="')+7:line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                if(firered_tutor_flag):
                    pokemon.firered_tutor_moves.append(Move(name))             
                if(emerald_tutor_flag):
                    pokemon.emerald_tutor_moves.append(Move(name))    
                if(xd_tutor_flag):
                    pokemon.xd_tutor_moves.append(Move(name))
                firered_tutor_flag = False
                emerald_tutor_flag = False
                xd_tutor_flag = False

    # revert directory to default
    os.chdir(src)

    print("tutor moves finished.")
    return output_pokemon_list

def populate_egg_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading egg moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "By_breeding"
        found_start_keyword = False

        found_move = False

        name = ""

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for moves in line
            if "_(move)" in line:
                found_move = True
                name = line[line.find('title="')+7:line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                pokemon.egg_moves.append(Move(name))

    # revert directory to default
    os.chdir(src)

    print("egg moves finished.")
    return output_pokemon_list

def populate_tm_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading tm moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "By_TM"
        found_start_keyword = False

        found_move = False

        name = ""

        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for moves in line
            if "_(move)" in line:
                found_move = True
                name = line[line.find('title="')+7:line.find(' (move)')]

            # add move to pokemon's move list
            if found_move:
                found_move = False
                pokemon.tm_moves.append(Move(name))

    # revert directory to default
    os.chdir(src)

    print("tm moves finished.")
    return output_pokemon_list

def populate_level_up_moves(input_pokemon_list):
    output_pokemon_list = input_pokemon_list
    print("loading level up moves.")

    # change directory for task
    os.chdir(scrape)

    for pokemon in output_pokemon_list:
        print(pokemon.name + ": " + str(round((pokemon.pokedex_number - 1) / 3.86, 2)) + "%")

        # open html source locally
        start_keyword = "By_leveling_up"
        found_start_keyword = False

        found_move = False

        name = ""

        temp_line = ""
        temp_line_emerald = ""
        temp_line_firered = ""
        emerald_level = -1
        firered_level = -1
        special_counter = -3
        counter = 0
        firered_flag = False


        temp_stored_page_read = open(str(pokemon.pokedex_number) + ".txt", "r", encoding="utf8")
        for line in temp_stored_page_read:
            # search for relevant section in page
            if "mw-headline" in line and found_start_keyword:
                break
            if start_keyword in line:
                found_start_keyword = True
            if not found_start_keyword:
                continue

            # search for the level associated with the move
            if "#9CD7C8" in line:
                firered_flag = True
                temp_line_emerald = line
            elif "#ACD36C" in line:
                firered_flag = True
                temp_line_firered = line
            elif "display:none" in line and "#D8D8D8" in line:
                temp_line_emerald = line

            # search for moves in line
            if "_(move)" in line:
                special_counter = counter
                temp_line = line
            elif "_(type)" in line and special_counter + 2 == counter:
                found_move = True
                special_counter = -3
                name = temp_line[temp_line.find('title="')+7:temp_line.find(' (move)')]
                # store level
                if firered_flag:
                    if "N/A" in temp_line_firered:
                        firered_level = -1
                    else:
                        firered_level = int(temp_line_firered[temp_line_firered.find("</span>")+7:])
                if "N/A" in temp_line_emerald:
                    emerald_level = -1
                else:
                    emerald_level = int(temp_line_emerald[temp_line_emerald.find("</span>")+7:])

            # add move to pokemon's move list
            if found_move:
                found_move = False
                if firered_flag:
                    pokemon.firered_level_up_moves.append(Move(name, firered_level))
                    pokemon.emerald_level_up_moves.append(Move(name, emerald_level))
                else:
                    pokemon.emerald_level_up_moves.append(Move(name, emerald_level))
            
            counter = counter + 1

    # revert directory to default
    os.chdir(src)

    print("level up moves finished.")
    return output_pokemon_list

    # I looked at the wiki page for this
    # and I decided coded a special case to read this was NOT worth it.
    # if I decide to add Deoxys form switching I will worry about it then.
def populate_deoxys_speed(pokemon):
    pokemon.emerald_level_up_moves.append(Move("Leer",1))
    pokemon.emerald_level_up_moves.append(Move("Wrap",1))
    pokemon.emerald_level_up_moves.append(Move("Night Shade",5))
    pokemon.emerald_level_up_moves.append(Move("Double Team",10))
    pokemon.emerald_level_up_moves.append(Move("Knock Off",15))
    pokemon.emerald_level_up_moves.append(Move("Pursuit",20))
    pokemon.emerald_level_up_moves.append(Move("Psychic",25))
    pokemon.emerald_level_up_moves.append(Move("Swift",30))
    pokemon.emerald_level_up_moves.append(Move("Agility",35))
    pokemon.emerald_level_up_moves.append(Move("Recover",40))
    pokemon.emerald_level_up_moves.append(Move("Psycho Boost",45))
    pokemon.emerald_level_up_moves.append(Move("ExtremeSpeed",50))

    pokemon.tm_moves.append(Move("Focus Punch"))
    pokemon.tm_moves.append(Move("Water Pulse"))
    pokemon.tm_moves.append(Move("Calm Mind"))
    pokemon.tm_moves.append(Move("Toxic"))
    pokemon.tm_moves.append(Move("Hidden Power"))
    pokemon.tm_moves.append(Move("Sunny Day"))
    pokemon.tm_moves.append(Move("Taunt"))
    pokemon.tm_moves.append(Move("Ice Beam"))
    pokemon.tm_moves.append(Move("Hyper Beam"))
    pokemon.tm_moves.append(Move("Light Screen"))
    pokemon.tm_moves.append(Move("Protect"))
    pokemon.tm_moves.append(Move("Rain Dance"))
    pokemon.tm_moves.append(Move("Safeguard"))
    pokemon.tm_moves.append(Move("Frustration"))
    pokemon.tm_moves.append(Move("SolarBeam"))
    pokemon.tm_moves.append(Move("Thunderbolt"))
    pokemon.tm_moves.append(Move("Thunder"))
    pokemon.tm_moves.append(Move("Return"))
    pokemon.tm_moves.append(Move("Psychic"))
    pokemon.tm_moves.append(Move("Shadow Ball"))
    pokemon.tm_moves.append(Move("Brick Break"))
    pokemon.tm_moves.append(Move("Double Team"))
    pokemon.tm_moves.append(Move("Reflect"))
    pokemon.tm_moves.append(Move("Shock Wave"))
    pokemon.tm_moves.append(Move("Rock Tomb"))
    pokemon.tm_moves.append(Move("Aerial Ace"))
    pokemon.tm_moves.append(Move("Torment"))
    pokemon.tm_moves.append(Move("Facade"))
    pokemon.tm_moves.append(Move("Secret Power"))
    pokemon.tm_moves.append(Move("Rest"))
    pokemon.tm_moves.append(Move("Skill Swap"))
    pokemon.tm_moves.append(Move("Snatch"))
    pokemon.tm_moves.append(Move("Cut"))
    pokemon.tm_moves.append(Move("Strength"))
    pokemon.tm_moves.append(Move("Flash"))
    pokemon.tm_moves.append(Move("Rock Smash"))

    pokemon.emerald_tutor_moves.append(Move("Body Slam"))
    pokemon.emerald_tutor_moves.append(Move("Counter"))
    pokemon.emerald_tutor_moves.append(Move("Double-Edge"))
    pokemon.emerald_tutor_moves.append(Move("Dream Eater"))
    pokemon.emerald_tutor_moves.append(Move("DynamicPunch"))
    pokemon.emerald_tutor_moves.append(Move("Endure"))
    pokemon.emerald_tutor_moves.append(Move("Fire Punch"))
    pokemon.emerald_tutor_moves.append(Move("Ice Punch"))
    pokemon.emerald_tutor_moves.append(Move("Icy Wind"))
    pokemon.emerald_tutor_moves.append(Move("Mega Kick"))
    pokemon.emerald_tutor_moves.append(Move("Mega Punch"))
    pokemon.emerald_tutor_moves.append(Move("Mimic"))
    pokemon.emerald_tutor_moves.append(Move("Mud-Slap"))
    pokemon.emerald_tutor_moves.append(Move("Psych Up"))
    pokemon.emerald_tutor_moves.append(Move("Rock Slide"))
    pokemon.emerald_tutor_moves.append(Move("Seismic Toss"))
    pokemon.emerald_tutor_moves.append(Move("Sleep Talk"))
    pokemon.emerald_tutor_moves.append(Move("Snore"))
    pokemon.emerald_tutor_moves.append(Move("Substitute"))
    pokemon.emerald_tutor_moves.append(Move("Swagger"))
    pokemon.emerald_tutor_moves.append(Move("Swift"))
    pokemon.emerald_tutor_moves.append(Move("ThunderPunch"))
    pokemon.emerald_tutor_moves.append(Move("Thunder Wave"))

    return pokemon


main()                