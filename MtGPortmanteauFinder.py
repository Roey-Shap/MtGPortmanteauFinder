import csv

# Notes:
# - Aside from just the largest portmanteau, it probably makes sense to include the largest *non-trival one*. Some names fit perfectly into others.
# - It's probably most coherent in terms of joke names if we limit portmantea-manship (?? Rolling with it) to full words matches.
#   ... that is, "Thing One" matches with "Never Give Up" to make "Thing Onever Give Up"... Not really the initial intention nor is it really effective.
# - Sort them by largest match afterwords, then write them into a file! 


def place_in_array(element, i, arr):
    return arr[0:i] + [element] + arr[i:-1]

def check_portmanteau_prefix(base_word, match_word):
    for i in range(min(len(base_word), len(match_word)), -1, -1):
        cur_slice = base_word[-(i+1):]
        if match_word.startswith(cur_slice):
            return cur_slice

    return ""

def get_best_portmanteau_match_for_name(suggested_card, card_names):
    # top_N_candidates: int = 1
    best_candidate_word = "No word"
    best_candidate_match = ""
    # best_candidates: list[tuple(str, str)] = [("None", "") for i in range(top_N_candidates)]
    for fuse_candidate in card_names:
        if fuse_candidate == suggested_card:
            continue

        fuse_candidate_prefix_slice = check_portmanteau_prefix(suggested_card, fuse_candidate)
        base_word_prefix_slice = check_portmanteau_prefix(fuse_candidate, suggested_card)

        best_successful_portmanteau_match = max(fuse_candidate_prefix_slice, base_word_prefix_slice, key=len)

        if len(best_successful_portmanteau_match) > len(best_candidate_match):
            best_candidate_match = best_successful_portmanteau_match
            best_candidate_word = fuse_candidate

        # if best_successful_portmanteau_match:
                        # for i, (prev_candidate, prev_candidate_match) in enumerate(best_candidates):
            #     # The list is sorted from greatest to smallest - 
            #     # so the first one we find that we defeat can be bumped down and that's all we need to check
            #     if len(prev_candidate_match) < len(best_successful_portmanteau_match):
            #         # print(best_candidates)
            #         best_candidates = place_in_array((fuse_candidate, best_successful_portmanteau_match), i, best_candidates)
            #         print(f"FOR {suggested_card} NEW CAND: {fuse_candidate}, MATCH: {best_successful_portmanteau_match}")
            #         break

    return (best_candidate_word, best_candidate_match)

def main():
    card_names: set[str] = set()
    with open('cards.csv', 'r', encoding="Latin1") as cards_csv:
        # raw_json_string = "".join(cards_json.readlines())
        # cards_data = json.load(cards_json)
        csv_reader = csv.DictReader(cards_csv)
        try:
            i = 1
            for row in csv_reader:
                new_name = row["name"].lower()
                if new_name not in card_names:
                   card_names.add(new_name)
                i += 1
        except Exception as e:
            print(f"There was an issue reading the name of row number {i}, stopping...")
            print(e)

    print(f"Number of cards loaded: {len(card_names)}")
    
    # suggested_card: str = ""
    # tried_once = False
    # found_card_in_database = False
    # while (not tried_once) or (not found_card_in_database):
    #     tried_once = True
    #     suggested_card = input("Input a card!\n").lower()
    #     found_card_in_database = suggested_card in card_names
    #     if not found_card_in_database:
    #         print(f"'{suggested_card}' isn't in the card database!")

    test_card = "rise of the dark realms"
    print(f"Best match for {test_card} is {get_best_portmanteau_match_for_name(test_card, card_names)}")

    portmanteau_matches: dict[str, tuple(str, str)] = {}
    for i, name in enumerate(card_names):
        if i < 50:
            portmanteau_matches[name] = get_best_portmanteau_match_for_name(name, card_names)
            i += 1
        else:
            break

    # print(f"\n\nTop {top_N_candidates} matches for {suggested_card}:")
    with open("./output.txt", "w") as output_file:
        for name in portmanteau_matches:
            matched_card, match = portmanteau_matches[name]
            print("{: <40}'s best match is ".format(name) + "{: <40}".format(matched_card) + " with match {: <20}".format(match), file=output_file)


if __name__ == "__main__":
    main()