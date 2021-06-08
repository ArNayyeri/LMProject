class StateNFA:
    def __init__(self, name, n):
        self.symbols = n
        self.name = name
        self.accept = False
        self.start = False
        self.map = [[] * n] * (n + 1)


class StateDFA:
    def __init__(self, name, n):
        self.symbols = n
        self.name = name
        self.accept = False
        self.start = False
        self.map = [[] * n] * n
        self.statesNFA = []
        self.check = False

    def __eq__(self, other):
        check = False
        for i in self.statesNFA:
            for j in other.statesNFA:
                if i == j:
                    check = True
                    break
            if not check:
                return False
        return True


class NFA:
    def __init__(self):
        self.states = []
        self.alpht = []
        self.accepts = []
        self.start = ''

    def __addState(self, state1, state2):
        for i in state1.map[state1.symbols]:
            self.__addState(i, state2)
        for i in range(len(self.alpht)):
            for j in state1.map[i]:
                state2.map[i].append(j)

    def __isExist(self, state):
        for i in self.states:
            if i == state:
                return True
        return False

    def convertDFA(self):
        dfa = DFA()
        dfa.alpht = self.alpht.copy
        dfa.start = StateDFA(self.start.name, len(self.alpht))
        dfa.start.statesNFA.append(self.start)
        dfa.states.append(dfa.start)
        count = 1
        for i in range(len(dfa.states)):
            for j in dfa.states[i].statesNFA:
                self.__addState(j, dfa.states[i])
                for k in dfa.states[i].map:
                    s = StateDFA('q' + str(count), len(self.alpht))
                    count = count + 1
                    s.statesNFA = k.copy
                    if not self.__isExist(s):
                        dfa.states.append(s)
                    else:
                        count = count - 1
        for i in dfa.states:
            for j in i.statesNFA:
                if j in self.accepts:
                    i.accept = True
                    break
        return dfa


class DFA:
    def __init__(self):
        self.states = []
        self.alpht = []
        self.accepts = []
        self.start = ''


a = NFA()
a.alpht = ['a', 'b']
q0 = StateNFA('q0', 2)
q1 = StateNFA('q1', 2)
q2 = StateNFA('q2', 2)
q0.map[0] = [q0, q1]
q0.map[1] = [q0]
q1.map[1] = [q2]
q0.start = True
q2.accept = True
a.start = q0
a.states = [q0, q1, q2]
a.accepts.append(q2)
e = a.convertDFA()
ee = e
