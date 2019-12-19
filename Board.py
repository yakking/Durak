import math
import Player
import Library
import random


# Board Class, Everything will be built on top of this.
class Board:
    def __init__(self, num_of_players=4, passed=True, winner_starts=True):
        """Initializes board.
        num_of_players: number of players that will play the game
        passed: whether you can pass cards in the game
        """
        # Checks if enough players are in the game
        if num_of_players < 2:
            # Raises error otherwise
            raise AttributeError("Can't Play with less than 2 people")
        # Calculates and keeps the number of players that are playing and the number of decks it needs to shuffle
        self.Num_of_players = num_of_players
        self.Num_of_decks = math.floor(num_of_players/5)
        # Creates Deck Object
        self.Current_Library = Library.Library(self.Num_of_decks)
        # Creates list of players
        self.Players = [Player.Player() for x in range(self.Num_of_players)]
        # Sets game type
        self.Passed = passed
        # Sets if the winner starts next game
        self.Winner_starts = winner_starts
        # Initializes all the unknown variables
        self.Trump_suit = None
        self.Current_attacker = 0
        self.Current_defender = 0
        self.Attack_zone = None
        self.Mode = None
        self.Winner = None
        self.Has_started_defending = None

    def start_game(self):
        """Stars game
        """
        # Shuffles Library
        self.Current_Library.shuffle_library()
        # Deals out 6 cards
        for x in range(6):
            # To each player
            for player in self.Players:
                player.add_card(self.Current_Library.get_next_card())
        # Sets the trump suit, as the bottom card.
        self.Trump_suit = self.Current_Library.bottom_card().Suit
        # Randomly chooses starting player
        self.Current_attacker = random.randint(0, self.Num_of_players - 1)
        # Sets game to attacking phase
        self.Mode = "A"
        # Sets the attack zone to empty
        self.Attack_zone = []

    def does_defend(self, attacking_card, defending_card):
        """Checks if defending card can defend the attacking card
        attacking_card: The attacking_card
        """
        # If defending card is trump card it beats any non trump card
        if defending_card.Suit == self.Trump_suit and attacking_card.Suit != self.Trump_suit:
            return True
        # If the defending card has the same suit as the attacking card
        elif defending_card.Suit == attacking_card.Suit:
            # Then if the defending card is higher rank it defends
            if defending_card.Rank > attacking_card.Rank:
                return True
            # Otherwise it doesn't
            else:
                return False
        # If the defending card has a non trump different suit it can't defend
        else:
            return False

    def first_attack(self,  list_of_card_indicies):
        if len(list_of_card_indicies) == 0:
            raise ValueError("Can't Attack with 0 cards")
        attacking_rank = self.Players[self.Current_attacker].hand[list_of_card_indicies[0]]
        for index in list_of_card_indicies:
            if self.Players[self.Current_attacker].hand[index] != attacking_rank:
                raise ValueError("Can't attack with multiple cards of different ranks")
        attacking_cards = self.Players[self.Current_attacker].play_cards(list_of_card_indicies)
        for card in attacking_cards:
            self.Attack_zone.append(card)
        self.Current_defender = (self.Current_attacker+1) % self.Num_of_players
        self.Mode = "D"


    def get_available_moves(self, player_index):
        # If its the attackers turn
        if self.Mode == "A":
            if player_index == self.Current_attacker:
                return list(range(self.Players[player_index].hand_size))
            else:
                return None

        """if self.Mode == "D":
            if"""





