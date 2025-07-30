code = """
%facts
owns(nono,m).
missile(m).
enemy(nono,america).
american(west).

%rules
sells(west,X,nono):-
    missile(X),owns(nono,X).
weapon(X):-
    missile(X).
hostile(X):-
    enemy(X,america).
criminal(X):-
    american(X),weapon(Y),sells(X,Y,Z),hostile(Z).

%Query
is_criminal(X):-
    criminal(X).

---------------------------------------------------

% Facts
man(marcus).
pompeian(marcus).

ruler(caesar).
tried_assassinate(marcus, caesar).

% Rules

roman(X) :- 
    pompeian(X).
loyal_to(X, caesar) :-
    roman(X),
    \+ tried_assassinate(X, caesar).

hate(X, caesar) :-
    roman(X),
    \+ loyal_to(X, caesar).

% Goal
did_hate(marcus, caesar) :-
    hate(marcus, caesar).

"""

def getCode():
    global code
    print(code)

    