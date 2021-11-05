"""Random player"""
from os import access
import random
from typing import Sequence

from environment.Constants import Action, Stage

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation
from utils.handValue import getHandPercent,getBoardHandType, getHandType
Scale = 1.2
# your bot class, rename to match the file name
class BotimusPrime(BotInterface):

    # change the name of your bot here
    def __init__(self, name="BotimusPrime"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space:Sequence[Action], observation:Observation) -> Action: 
        '''
            This function gets called whenever it's your bots turn to act.
                Parameters:
                    action_space (Sequence[Action]): list of actions you are allowed to take at the current state. 
                    observation (Observation): all information available to your bot at the current state. See environment/Observation for details
                returns:
                    action (Action): the action you want you bot to take. Possible actions are: FOLD, CHECK, CALL and RAISE
            If this function takes longer than 1 second, your bot will fold
        '''
        

        
         # use different strategy depending on pre or post flop (before or after community cards are delt)
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        last_action = opponent_actions_this_round[-1] if len(
            opponent_actions_this_round) > 0 else None
        
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation, last_action)

        return self.handlePostFlop(observation, last_action)

    def handlePreFlop(self, observation: Observation, last_action: Action) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < 0.7*Scale:
            return Action.RAISE
        if handPercent < 0.4*Scale:        
            return Action.CALL
        return Action.FOLD
        
        

    def handlePostFlop(self, observation: Observation, last_action: Action) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        boardhandtype = getBoardHandType(observation.boardCards)
        myhandtype, _ = getHandType(observation.myHand,observation.boardCards)        
        
        if handPercent < 0.7*Scale:
            return Action.RAISE
        if handPercent < 0.4*Scale:        
            return Action.CALL
        return Action.FOLD


