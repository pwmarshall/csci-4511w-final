"""Contains a Bot that plays checkers using MCTS.

(CC) 2025 Peter Marshall, Minneapolis, Minnesota
pwmarshall@gmail.com
"""
import random
from collections import defaultdict
import math
import threading
import copy
from checkers.board import Board, BoardHash, Board_State
from checkers.player import Player
import checkers.constants as constant
from datetime import datetime
from checkers.display import Display
time_check = False

def r0():
    global time_check
    time_check = True
    print("Too long of a game")
    return 

#General implementation of MCTS, would work for any node class, modified slightly for 2 player
class MCTS2:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, player: Player, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children: dict[BoardHash, set[Board]] = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.timer = threading.Timer(5.0, r0)
        self.player = player

    def choose(self, node: BoardHash):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            print("It choose Random")
            return node.find_random_child(node.board)
        
        optionsNQ: list[tuple[int, int]] = []

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            
            qval = self.Q[n]  # total reward of this node
            nval = self.N[n]  # total visits of this node

            if constant.PRINT_INFO: print(qval, " / ", nval, " = ", qval / nval) #Avg reward per state
            optionsNQ.append((nval,qval))

            return qval / nval
        #Chooses the node with the highest avg reward
        return max(self.children[node], key=score),optionsNQ

    def do_rollout(self, node: BoardHash):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node: BoardHash):
        "Find an unexplored descendent of `node`"
        path: list[BoardHash] = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node: BoardHash):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children(self.player)
        for child in self.children[node]:
            self.children[child] = child.find_children(self.player.other)

    def _simulate(self, node: BoardHash):
        global time_check
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        self.timer = threading.Timer(2.5,r0)
        self.timer.start()
        while True:
            if node.is_terminal():
                reward = node.reward(self.player)
                self.timer.cancel()
                return reward
                #return 1 - reward if invert_reward else reward
            if time_check:
                time_check = False
                return 0
            node = node.find_random_child(self.player)
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):

            self.N[node] += 1
            if not node.is_terminal():
                reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa
            self.Q[node] += reward

    def _uct_select(self, node: BoardHash):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        #assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])
        #This is the log of the total visits in Node

        def uct(n):
            "Upper confidence bound for trees"
            if self.N[n] == 0:
                return 999
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)
    

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.timer = threading.Timer(5.0, r0)

    def choose(self, node: Board_State):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal(node.board):
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            print("It chose Random")
            return node.find_random_child(node.board)
        
        optionsNQ = []

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            
            qval = self.Q[n]  # total reward of this node
            nval = self.N[n]  # total visits of this node

            if constant.PRINT_INFO: print(qval, " / ", nval, " = ", qval / nval) #Avg reward per state
            optionsNQ.append((nval,qval))

            return qval / nval
        #Chooses the node with the highest avg reward
        return max(self.children[node], key=score),optionsNQ

    def do_rollout(self, node: Board_State):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node: Board_State):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node: Board_State):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children(node.board)
        for child in self.children[node]:
            self.children[child] = node.find_oppchildren(child.board)

    def _simulate(self, node: Board_State):
        global time_check
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        self.timer = threading.Timer(2.5,r0)
        self.timer.start()
        while True:
            if node.is_terminal(node.board):
                reward = node.reward(node.board)
                self.timer.cancel()
                return reward
                #return 1 - reward if invert_reward else reward
            if time_check:
                time_check = False
                return 0
            node = node.find_random_child(node.board)
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):

            self.N[node] += 1
            if not node.is_terminal(node.board):
                reward = 1- reward  # 1 for me is 0 for my enemy, and vice versa
            self.Q[node] += reward

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        #assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])
        #This is the log of the total visits in Node

        def uct(n):
            "Upper confidence bound for trees"
            if self.N[n] == 0:
                return 999
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

class MCTSBot:
    """Bot that selects a move given a checkers board state.

    It is implemented with a MCTS algorithm. 

    Attributes
    ----------
    player : Player
        Player that this bot is. It could be white or black.
    rollouts : int (Default = 10)
        The number of rollouts that MCTS does each turn to explore/train the tree. More rollouts will
        make the system better, but it will also take longer to process.
    """

    def __init__(self, player, rollouts = 100):
        """Initiates the bot.

        Parameters
        ----------
        player : Player
            Player that this bot is. It could be white or black.

        """
        self.player = player
        self.rollouts = rollouts
        self.tree = MCTS()
        self.avgRlist = []

    def reset_tree(self):
        self.tree = MCTS()
        self.avgRlist = []

    def select_move(self, board: Board):
        """Selects a random move given a board state.

        Parameters
        ----------
        board : Board
            Current board state, with a position and a list of possible moves.

        Returns
        --------
        Move [(int, int), (int, int), Pieces[]]
            Move selected from explored MCTS tree.

        """
        boardHash = Board_State(board.board)
        last_time = datetime.now()

        for i in range(self.rollouts):
            self.tree.do_rollout(boardHash)
            if constant.PRINT_INFO:
                if i % 50 == 0 and i != 0:
                    seconds = (datetime.now() - last_time).microseconds / 1000000.0
                    simtime = 50.0 / seconds
                    print("Simulation speed: %2.2f" %(simtime), "g/s")
                    last_time = datetime.now()


        choice, optionsNQ = self.tree.choose(boardHash) 

        def avgRmethod(o):
            return o[1] / o[0]
        bestavgR = max(optionsNQ, key=avgRmethod)
        self.avgRlist.append((int(bestavgR[1] / bestavgR[0] * 10000) / 10000))

        nsum = 0
        for option in optionsNQ:
            nsum += option[0]

        if constant.PRINT_INFO: print(self.avgRlist)

        return choice.parentMove
