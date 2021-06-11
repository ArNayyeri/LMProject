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
        self.start = None

    def __addState(self, state1, state2, count):
        for i in state1.map[state1.symbols]:
            if not state2.statesNFA.__contains__(i):
                self.__addState(i, state2, count)
        for i in range(len(self.alpht)):
            m = []
            for j in state1.map[i]:
                m.append(j)
            if len(m) == 0:
                continue
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
        dfa.alpht = self.alpht
        dfa.start = StateDFA(self.start.name, len(self.alpht))
        dfa.start.statesNFA.append(self.start)
        dfa.states.append(dfa.start)
        dfa.start.start = True
        count = 1
        i = 0
        while i < len(dfa.states):
            for j in dfa.states[i].statesNFA:
                self.__addState(j, dfa.states[i], count)
            for k in range(len(dfa.states[i].map)):
                x = self.__isExist(dfa, dfa.states[i].map[k])
                if x == -1:
                    if isinstance(dfa.states[i].map[k], StateDFA):
                        dfa.states.append(dfa.states[i].map[k])
                else:
                    dfa.states[i].map[k] = dfa.states[x]
            i = i + 1

        for i in dfa.states:
            for j in range(len(i.map)):
                if i.map[j] == []:
                    if dfa.trap is None:
                        t = StateNFA('∅', len(self.alpht))
                        dfa.trap = StateDFA('∅', len(self.alpht))
                        dfa.states.append(dfa.trap)
                        dfa.trap.statesNFA.append(t)
                        dfa.trap.map[0] = dfa.trap
                        dfa.trap.map[1] = dfa.trap
                    i.map[j] = dfa.trap
        r = 1
        for i in dfa.states:
            if i.name != '∅':
                i.name = 'q' + str(r)
                r = r + 1
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
        self.start = None
        self.trap = None

    def getstate(self, name):
        for i in self.states:
            if name == i.name:
                return i
        return None

    def minimization(self):
        a = MinimizationPart(len(self.alpht))
        b = MinimizationPart(len(self.alpht))

        for i in self.states:
            if i.accept:
                a.states.append(i.name)
            else:
                b.states.append(i.name)
        p0 = [a, b]
        p1 = []

        while True:
            for i in p0:
                for j in i.states:
                    q = self.getstate(j)
                    w = MinimizationPart(len(self.alpht))
                    w.states.append(j)
                    for k in q.map:
                        for l in p0:
                            if l.states.__contains__(k.name):
                                w.map.append(l)
                    check = True
                    for k in p1:
                        if k.check(w):
                            k.states.append(j)
                            check = False
                            break
                    if check:
                        p1.append(w)
            if len(p0) == len(p1):
                break
            p0 = p1
            p1 = []
        for i in p1:
            for j in range(len(i.map)):
                for k in p1:
                    if k.check2(i.map[j]):
                        i.map[j] = k
        self.accepts.clear()
        self.trap = None
        for i in range(len(p1)):
            p1[i].stateD.name = 'q' + str(i)
            p1[i].stateD.map.clear()
            for j in p1[i].states:
                q = self.getstate(j)
                if q.start:
                    p1[i].stateD.start = True
                    self.start = p1[i].stateD
                if q.accept:
                    p1[i].stateD.accept = True
                    self.accepts.append(p1[i].stateD)
            for j in p1[i].map:
                p1[i].stateD.map.append(j.stateD)
        self.states.clear()
        for i in p1:
            self.states.append(i.stateD)

    def checkstring(self, string):
        q = self.start
        for i in string:
            q = q.map[self.alpht.index(i)]
        return q.accept


class MinimizationPart:
    def __init__(self, size):
        self.states = []
        self.map = []
        self.stateD = StateDFA('', size)

    def check(self, other):
        if len(self.map) != len(other.map):
            return False
        for i in range(len(self.map)):
            if self.map[i] != other.map[i]:
                return False
        return True

    def check2(self, other):
        if len(self.states) != len(other.states):
            return False
        for i in self.states:
            check = True
            for j in other.states:
                if i == j:
                    check = False
                    break
            if check:
                return False
        return True
