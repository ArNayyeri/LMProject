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

    def __eq__(self, other):
        if not isinstance(other, StateDFA) or len(self.statesNFA) != len(other.statesNFA):
            return False
        for i in self.statesNFA:
            check = False
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

    def __addState(self, state1, state2, count):
        for i in state1.map[state1.symbols]:
            if not state2.statesNFA.__contains__(i):
                self.__addState(i, state2, count)
        for i in range(len(self.alpht)):
            m = []
            for j in state1.map[i]:
                m.append(j)
            if isinstance(state2.map[i], StateDFA):
                for k in m:
                    if not state2.map[i].statesNFA.__contains__(k):
                        state2.map[i].statesNFA.append(k)
            else:
                s = StateDFA('q' + str(count), len(self.alpht))
                count = count + 1
                s.statesNFA = m
                state2.map[i] = s

    def __isExist(self, dfa, state):
        for i in range(len(dfa.states)):
            if dfa.states[i] == state:
                return i
        return -1

    def convertDFA(self):
        dfa = DFA()
        dfa.alpht = self.alpht.copy
        dfa.start = StateDFA(self.start.name, len(self.alpht))
        dfa.start.statesNFA.append(self.start)
        dfa.states.append(dfa.start)
        count = 1
        i = 0
        while i < len(dfa.states):
            for j in dfa.states[i].statesNFA:
                self.__addState(j, dfa.states[i], count)
            for k in range(len(dfa.states[i].map)):
                x = self.__isExist(dfa, dfa.states[i].map[k])
                if x == -1:
                    dfa.states.append(dfa.states[i].map[k])
                else:
                    dfa.states[i].map[k] = dfa.states[x]
            i = i + 1

        for i in dfa.states:
            for j in i.statesNFA:
                if j in self.accepts:
                    i.accept = True
                    dfa.accepts.append(i)
                    break
        return dfa


class DFA:
    def __init__(self):
        self.states = []
        self.alpht = []
        self.accepts = []
        self.start = ''


def printdfa(e):
    for i in e.states:
        for j in i.statesNFA:
            print(j.name + ',', end='')
        print('  ', end='')
        for j in i.map:
            for k in j.statesNFA:
                print(k.name + ',', end='')
            print('  ', end='')
        print()


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
#printdfa(e)

b = NFA()
b.alpht = ['0', '1']
q0 = StateNFA('q0', 2)
q1 = StateNFA('q1', 2)
q2 = StateNFA('q2', 2)
q0.map[0] = [q0]
q0.map[1] = [q1]
q1.map[0] = [q1, q2]
q1.map[1] = [q1]
q2.map[0] = [q2]
q2.map[1] = [q1, q2]
q0.start = True
q2.accept = True
b.start = q0
b.states = [q0, q1, q2]
b.accepts.append(q2)
bb = b.convertDFA()
printdfa(bb)
