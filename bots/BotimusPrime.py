"""Random player"""
from os import access
import random
from typing import Sequence

from environment.Constants import Action, Stage

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation
from utils.handValue import getHandPercent,getBoardHandType, getHandType
Percent = 0.6
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
        if last_action is None:
            if handPercent < Percent *2:
                return Action.RAISE
            return Action.CALL
        if last_action is Action.RAISE:
            if handPercent < Percent*0.5:
                Action.RAISE
            if handPercent < Percent *2:
                Action.CALL
            return Action.FOLD
        if last_action in [Action.CHECK, Action.CALL]:
            if handPercent < Percent *3:
                return Action.RAISE
            return Action.CALL
        
        

    def handlePostFlop(self, observation: Observation, last_action: Action) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        boardhandtype = getBoardHandType(observation.boardCards)
        myhandtype, _ = getHandType(observation.myHand,observation.boardCards)
        rage = 0
        if boardhandtype.value < myhandtype.value:
            rage = 1
        # if my hand is top 30 percent: raise
        if last_action is None:
            if rage == 1:                
                if handPercent < Percent *2:
                    return Action.RAISE
                if handPercent < Percent *3.5:
                    return Action.CHECK
            if handPercent < Percent:
                return Action.RAISE
            return Action.CHECK
            # opponent didn't do anything yet for us to counter, just raise            
        elif last_action in [Action.CHECK, Action.CALL]:
            if rage == 1:                
                if handPercent < Percent*1.5:
                    return Action.RAISE
                if handPercent < Percent*2.5:
                    return Action.CHECK
            if handPercent < Percent:
                return Action.RAISE
            return Action.CHECK
        elif last_action == Action.RAISE:
            if rage == 1:                
                if handPercent < Percent:
                    return Action.RAISE
                if handPercent < Percent*1.5:
                    return Action.CHECK
            if handPercent < Percent*0.5:
                return Action.RAISE
            if handPercent < Percent*2:
                return Action.RAISE
            return Action.FOLD