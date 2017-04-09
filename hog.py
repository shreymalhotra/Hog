"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    total, outcome_is_one = 0, False
    while num_rolls > 0:
        each_roll = dice()
        if each_roll == 1:
            outcome_is_one = True
        else:
            total += each_roll
        num_rolls -= 1
    if outcome_is_one is True:
        return 0
    return total
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    def is_prime(n):
        check_n_prime = 2
        if n == 1 or n == 0:
            return False
        else:
            while check_n_prime < n:
                if n % check_n_prime == 0:
                    return False
                else:
                    check_n_prime += 1
            return True

    def next_prime(n):
        while True:
            n += 1
            counter = 2
            while counter < n:
                if is_prime(n) == True:
                    return n 
                else:
                    counter += 1

    if num_rolls != 0:
    	temp = roll_dice(num_rolls, dice)
    if num_rolls == 0:
        max_return = (1 + int(max(list(str(opponent_score)))))
        if is_prime(max_return) == True:
        	return next_prime(max_return)
        else:
        	return max_return
    elif (is_prime(temp) == True):
        return next_prime(temp)
    else:
        return temp
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    from operator import add, floordiv
    seven_div = (opponent_score + score) % 7 == 0
    if seven_div:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if ((score0 // 10) % 10) == (score1 % 10) and ((score1 // 10) % 10) == (score0 % 10):
        return True
    else:
        return False
    # END Question 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    
    # BEGIN Question 5
    def player_turn(player_score, opponent_score, player_strategy, opponent_strategy):
        current_score = take_turn(player_strategy(player_score, opponent_score), 
            opponent_score, select_dice(player_score, opponent_score))
        if current_score == 0:
            opponent_score += player_strategy(player_score, opponent_score)
            # return opponent_score
        else:
            player_score += current_score
        return (opponent_score, player_score)
            # return player_score

    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    
    while score0 < goal and score1 < goal:
        if player == 0:
            score1, score0 = player_turn(score0, score1, strategy0, strategy1)
        else:
            score0, score1 = player_turn(score1, score0, strategy1, strategy0)
        
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        player = other(player)
    return score0, score1
    
    # END Question 5
#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    from operator import add, truediv
    def average_argument(*args):
        sum_of_args = 0
        n = 0
        while n < num_samples:
            sum_of_args += fn(*args)
            n += 1
        return truediv(sum_of_args,num_samples)
    return average_argument
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    max_average = 0
    num_rolls = 1
    for count in range(1,11):
        each_average = make_averaged(roll_dice)(count, dice)
        if each_average > max_average:
            max_average = each_average
            num_rolls = count
    return num_rolls
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    if take_turn(0, opponent_score) >= margin:
        return 0
    else:
        return num_rolls  
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    score += take_turn(0, opponent_score)
    if score < opponent_score:
        if is_swap(score, opponent_score):
            return 0
        else:
            return num_rolls
    else:
        return num_rolls
    # END Question 9


    """This final strategy implements the swap_strategy and the bacon_strategy 
    to decide how whether 0 or 4 num_rolls should be returned. This strategy 
    makes sure to use only beneficial swaps.
    """
   # BEGIN Question 10
    if (swap_strategy(score, opponent_score)) == 0:
        return 0
    elif (bacon_strategy(score, opponent_score)) == 0:
        if score > opponent_score and is_swap(opponent_score, score + take_turn(0, opponent_score) ) == True:
            return 4
        return 0
    elif score >= 40:
        return bacon_strategy(score,opponent_score, 5, 3)
    elif (score + opponent_score) % 7 == 0:
        return bacon_strategy(score, opponent_score, 3, 2)
    return 4
    # END Question 10

##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()