"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    selected_paragraphs = [ps for ps in paragraphs if select(ps) == True]
    if k > len(selected_paragraphs) - 1:
        return ''
    else:
        return selected_paragraphs[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def about_topic(paragraph):
        for tpc in topic:
            if tpc in split(lower(remove_punctuation(paragraph))):
                return True
        return False
    return about_topic
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    total_words = len(typed_words)
    if total_words == 0:
        return 0.0
    correct_words = 0
    for i in range(len(reference_words)):
        if i >= total_words:
            break
        if typed_words[i] == reference_words[i]:
            correct_words += 1
    return correct_words / total_words * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    characters_length = len(typed)
    words = characters_length / 5
    return words * 60 / elapsed
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    def get_word(user_word, valid_words, diff_function, limit):
        target_word = user_word
        target_diff = limit
        for i in range(len(valid_words)):
            if diff_function(user_word, valid_words[i], limit) < target_diff:
                target_diff = diff_function(user_word, valid_words[i], limit)
                target_word = valid_words[i]
            elif diff_function(user_word, valid_words[i], limit) == target_diff and target_diff == limit:
                return get_first_word(user_word, valid_words[i+1:], diff_function, limit, valid_words[i])
        return target_word

    def get_first_word(user_word, valid_words, diff_function, limit, first_word):
        target_word = first_word
        target_diff = limit
        for i in range(len(valid_words)):
            if diff_function(user_word, valid_words[i], limit) < target_diff:
                target_diff = diff_function(user_word, valid_words[i], limit)
                target_word = valid_words[i]
        return target_word

    if user_word in valid_words:
        return user_word
    else:
        return get_word(user_word, valid_words, diff_function, limit)
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def f(start, goal, count, limit):
        if len(start) == 0 or len(goal) == 0:
            return abs(len(start) - len(goal)) + count
        if count > limit:
            return count
        elif start[0] == goal[0]:
            return f(start[1:], goal[1:], count, limit)
        elif start[0] != goal[0]:
            return f(start[1:], goal[1:], count+1, limit)
    return f(start, goal, 0, limit)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if start == goal: # Fill in the condition
        # BEGIN
        return 0
        # END

    elif limit == -1:
        return 0

    elif len(start) == 0 or len(goal) == 0:
        return abs(len(start) - len(goal))

    elif start[0] == goal[0]: # Feel free to remove or add additional cases
        # BEGIN
        return pawssible_patches(start[1:], goal[1:], limit)
        # END

    else:
        add_diff = lambda start, goal, limit: 1 + pawssible_patches(start, goal[1:], limit-1)# Fill in these lines
        remove_diff = lambda start, goal, limit: 1 + pawssible_patches(start[1:], goal, limit-1)
        substitute_diff = lambda start, goal, limit: 1 + pawssible_patches(start[1:], goal[1:], limit-1)
        # BEGIN
        return min(add_diff(start, goal, limit), remove_diff(start, goal, limit), substitute_diff(start, goal, limit))
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    def point(typed, prompt):
        if prompt == []:
            return 0
        elif typed == []:
            return 0
        elif typed[0] == prompt[0]:
            return 1 + point(typed[1:], prompt[1:])
        else:
            return 0

    send({'id': user_id, 'progress': point(typed, prompt)/len(prompt)})
    return point(typed, prompt) / len(prompt)
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    def to_times(times_per_player):
        if times_per_player == []:
            return []
        else:
            time = []
            for i in range(len(times_per_player[0])-1):
                time.append(times_per_player[0][i+1]-times_per_player[0][i])
            return [time] + to_times(times_per_player[1:])

    return game(words, to_times(times_per_player))
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    res = []
    for _ in player_indices:
        res.append([])
    for word_index in word_indices:
        t = time(game, 0, word_index)
        player = 0
        for player_num in player_indices:
            if time(game, player_num, word_index) < t:
                t = time(game, player_num, word_index)
                player = player_num
        res[player].append(word_at(game, word_index))
    return res
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
