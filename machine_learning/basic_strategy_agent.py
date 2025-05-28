class BasicStrategyAgent:
    def act(self, player_sum, dealer_card, is_soft, num_cards):
        dealer = 11 if dealer_card == 1 else dealer_card

        if is_soft:
            if 12 <= player_sum <= 16:
                return 'hit'
            elif player_sum == 17:
                return 'stand'
            elif player_sum == 18:
                if dealer in [2, 7, 8]:
                    return 'stand'
                else:
                    return 'hit'
            elif player_sum >= 19:
                return 'stand'
            else:
                return 'hit' 
        else:
            if 4 <= player_sum <= 8:
                return 'hit'
            elif player_sum == 9:
                if dealer in [3,4,5,6]:
                    return 'hit'  
                else:
                    return 'hit'
            elif player_sum == 10:
                if dealer in [2,3,4,5,6,7,8,9]:
                    return 'hit'  
                else:
                    return 'hit'
            elif player_sum == 11:
                return 'hit'  
            elif player_sum == 12:
                if dealer in [4,5,6]:
                    return 'stand'
                else:
                    return 'hit'
            elif player_sum == 13 or player_sum == 14:
                if dealer in [2,3,4,5,6]:
                    return 'stand'
                else:
                    return 'hit'
            elif player_sum == 15:
                if dealer in [2,3,4,5,6]:
                    return 'stand'
                else:
                    return 'hit'
            elif player_sum == 16:
                if dealer in [2,3,4,5,6]:
                    return 'stand'
                else:
                    return 'hit'
            else:  
                return 'stand'
