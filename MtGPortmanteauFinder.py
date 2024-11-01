import csv
import time
import cython

# Notes:
# Considered also disqualifing any matches that are in the list of cards, but whatver it's a consequence.
# Statistics you could track for each card:
#   How many times has it been used in a match?
#   All of the matches of the top size it found / Number of times it matched of that size

def place_in_array(element, i, arr):
    return arr[0:i] + [element] + arr[i:-1]

def check_portmanteau_prefix(name1, name2):
    for i in range(min(len(name1), len(name2)), -1, -1):
        cur_slice = name1[-(i+1):]
        if name2.startswith(cur_slice):
            return cur_slice

    return ""

def check_portmanteau_prefix_whole_word(name1, name2):
    split1 = name1.split()
    split2 = name2.split()
    largest_matching_subset = None
    for i in range(min(len(split1), len(split2))-1, -1, -1):
        slice1 = split1[-(i+1):]
        last_matching_index = -1
        found_mismatching_word_in_name2 = False
        for j in range(i+1):
            if slice1[-(j+1)] != split2[i-j]:
                found_mismatching_word_in_name2 = True
                break
            else:
                last_matching_index = j
        if not found_mismatching_word_in_name2:
            largest_matching_subset = last_matching_index

    if largest_matching_subset is not None:
        return " ".join(split1[-(largest_matching_subset+1):])
    else:
        return ""

def get_best_portmanteau_match_for_name(suggested_card, card_names, whole_word_mode, get_top_N_match_sizes=1, num_matches_per_size=1):
    best_candidate_word = "No word"
    best_candidate_match = ""
    # ranked_matches: dict[str, tuple[]]
    portmanteau_check_function = check_portmanteau_prefix_whole_word if whole_word_mode else check_portmanteau_prefix

    for fuse_candidate in card_names:
        # Remove trivial solutions
        if fuse_candidate in suggested_card or suggested_card in fuse_candidate:
            continue

        fuse_candidate_prefix_slice = portmanteau_check_function(suggested_card, fuse_candidate)
        if fuse_candidate_prefix_slice in card_names:
            fuse_candidate_prefix_slice = ""

        base_word_prefix_slice = portmanteau_check_function(fuse_candidate, suggested_card)
        if base_word_prefix_slice in card_names:
            base_word_prefix_slice = ""


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
    FILE_ENCODING = "Latin1"
    
    card_names: set[str] = set()
    with open('cards.csv', 'r', encoding=FILE_ENCODING) as cards_csv:
        csv_reader = csv.DictReader(cards_csv)
        try:
            i = 1
            for row in csv_reader:
                new_names = row["name"].lower().split("//")
                for new_name in new_names:
                    new_name = new_name.strip()
                    if len(new_name) > 0 and new_name not in card_names:
                        card_names.add(new_name)
                        i += 1
        except Exception as e:
            print(f"There was an issue reading the name of row number {i}, stopping...")
            print(e)

    print(f"Number of cards loaded: {len(card_names)}")
    
    suggested_card: str = ""
    tried_once = False
    found_card_in_database = False
    while (not tried_once) or (not found_card_in_database):
        tried_once = True
        suggested_card = input("Input a card!\n").lower()
        found_card_in_database = suggested_card in card_names
        if not found_card_in_database:
            print(f"'{suggested_card}' isn't in the card database!")

    print(f"Best match for {suggested_card} is {get_best_portmanteau_match_for_name(suggested_card, card_names, False)}") # , get_top_N_match_sizes=5, num_matches_per_size=5

    print("Starting timer...")
    start_time = time.time()

    portmanteau_matches: dict[str, tuple(str, str)] = {}
    portmanteau_matches_whole_word: dict[str, tuple(str, str)] = {}
    for i, name in enumerate(card_names):
        portmanteau_matches[name]               = get_best_portmanteau_match_for_name(name, card_names, False)
        portmanteau_matches_whole_word[name]    = get_best_portmanteau_match_for_name(name, card_names, True)
        if i % 100 == 0:
            print(f"Index {i + 1} at {round(time.time() - start_time)} seconds")
    
    # print(f"\n\nTop {top_N_candidates} matches for {suggested_card}:")

    ordered_portmanteau_matches = [(name, best_candidate_name, candidate_match) for name, (best_candidate_name, candidate_match) in portmanteau_matches.items()]
    ordered_portmanteau_whole_word_matches = [(name, best_candidate_name, candidate_match) for name, (best_candidate_name, candidate_match) in portmanteau_matches_whole_word.items()]

    ordered_portmanteau_matches.sort(key=lambda tuple: len(tuple[2]), reverse=True)
    ordered_portmanteau_whole_word_matches.sort(key=lambda tuple: len(tuple[2]), reverse=True)
    # print(ordered_portmanteau_matches)
    
    with open("./output_anything_goes.txt", "w", encoding=FILE_ENCODING) as output_file:
        for name, matched_card, match in ordered_portmanteau_matches:
            print("{: <40}'s best match is ".format(name) + "{: <40}".format(matched_card) + " with match {: <20}".format(match), file=output_file)

    with open("./output_whole_word.txt", "w", encoding=FILE_ENCODING) as output_file:
        for name, matched_card, match in ordered_portmanteau_whole_word_matches:
            print("{: <40}'s best match is ".format(name) + "{: <40}".format(matched_card) + " with match {: <20}".format(match), file=output_file)


if __name__ == "__main__":
    main()