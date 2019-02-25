from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        #numofPegs = len(self.kb.kb_ask(parse_input("fact: (is ?x peg")))
        result = []
        for pegNum in range(1, 4):
            pegStr = "peg" + str(pegNum)
            pegQ = "fact: (on ?x peg)".replace("peg", pegStr)
            pegAsk = parse_input(pegQ)
            bindingslist = self.kb.kb_ask(pegAsk)
            pegList = []
            if bindingslist:
                for bindings in bindingslist:
                    #current = bindings.bindings[0].constant.element[4:]
                    #if bindings['?x'] in current:
                    diskstr = bindings['?x']
                    pegList.append(int(diskstr[-1]))
            pegList.sort()
            result.append(tuple(pegList))
        return tuple(result)




    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # student code goes here
        startPeg = str(movable_statement.terms[1])
        startPegNum = int(startPeg[-1])
        endPeg = str(movable_statement.terms[2])
        endPegNum = int(endPeg[-1])
        game_state = self.getGameState()
        disk = str(movable_statement.terms[0])

        startPeg_state = game_state[startPegNum - 1]
        endPeg_state = game_state[endPegNum - 1]


        # check if endPeg was empty before move
        if len(endPeg_state) == 0:
            self.kb.kb_retract(parse_input("fact: (empty " + endPeg + ")"))
        else:
            # retract top of ending peg
            self.kb.kb_retract(parse_input("fact: (top disk" + str(endPeg_state[0]) + ' ' + endPeg + ")"))
        # retract top of starting peg
        self.kb.kb_retract(parse_input("fact: (top " + disk + ' ' + startPeg + ")"))
        # retract on starting peg
        self.kb.kb_retract(parse_input("fact: (on " + disk + ' ' + startPeg + ")"))
        #assert top of ending peg
        self.kb.kb_assert(parse_input("fact: (top " + disk + ' ' + endPeg + ")"))
        #assert on ending peg
        self.kb.kb_assert(parse_input("fact: (on " + disk + ' ' + endPeg + ")"))

        # check if starting peg is empty
        if len(startPeg_state) > 1:
            # assert new top of starting peg
            self.kb.kb_assert(parse_input("fact: (top disk" + str(startPeg_state[1]) + ' ' + startPeg + ")"))
        else:
            # assert starting peg empty
            self.kb.kb_assert(parse_input("fact: (empty " + startPeg + ")"))

    # rule: ((top ?x ?peg1)(empty ?peg2)) -> (movable ?x ?peg1 ?peg2)
    # rule: ((top ?x ?peg1)(top ?y ?peg2)(larger ?y ?x)) -> (movable ?x ?peg1 ?peg2)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        result = []
        # peg1list = []
        # peg2list = []
        # peg3list = []
        game_map = {}
        for y in range(1, 4):
            temp = []
            for x in range(1, 4):
                ask = "fact: (loc ?tile pos" + str(x) + " pos" + str(y) + ')'
                bindings = self.kb.kb_ask(parse_input(ask))
                if bindings:
                    for binding in bindings:
                        if binding["?tile"] not in game_map:
                            if binding["?tile"] == "empty":
                                game_map[binding["?tile"]] == -1
                            else:
                                game_map[binding["?tile"]] == int(binding["?tile"][-1])
                        temp.append(game_map[bindings["?tile"]])
            result.append(tuple(temp))
        return tuple(result)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        tile = str(movable_statement.terms[0])
        startx = str(movable_statement.terms[1])
        starty = str(movable_statement.terms[2])
        endx = str(movable_statement.terms[3])
        endy = str(movable_statement.terms[4])

        fact_ret1 = "fact: (at " + tile + " " + startx + " " + starty + ")"
        self.kb.kb_retract(parse_input(fact_ret1))

        fact_ret2 = "fact: (at empty " + endx + " " + endy + ")"
        self.kb.kb_retract(parse_input(fact_ret2))

        fact_assert1 = "fact: (at " + tile + " " + endx + " " + endy + ")"
        self.kb.kb_assert(parse_input(fact_assert1))

        fact_assert2 = "fact: (at empty " + startx + " " + starty + ")"
        self.kb.kb_assert(parse_input(fact_assert2))

    # rule: ((at ?tileA ?x pos2)(at ?tileB ?x ?y)) -> (adjacent ?tileA ?tileB)
    # rule: ((at ?tileA pos2 ?y)(at ?tileB ?x ?y)) -> (adjacent ?tileA ?tileB)
    # rule: ((at ?tileA ?x ?y)(at ?tileB pos2 ?y)) -> (adjacent ?tileA ?tileB)
    # rule: ((at ?tileA ?x ?y)(at ?tileB ?x pos2)) -> (adjacent ?tileA ?tileB)
    # rule: ((at empty ?x pos2)(at ?tileB ?x ?y)) -> (movable ?tileB ?x ?y ?x pos2)
    # rule: ((at empty pos2 ?y)(at ?tileB ?x ?y)) -> (movable ?tileB ?x ?y pos2 ?y)
    # rule: ((at empty ?x ?y)(at ?tileB ?x pos2)) -> (movable ?tileB ?x pos2 ?x ?y)
    # rule: ((at empty ?x ?y)(at ?tileB pos2 ?y)) -> (movable ?tileB pos2 ?y ?x ?y)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
