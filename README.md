# State Machines

# what am it?

* a thing which is in only one state at a given time, 
* in response to some input it transitions to a new state
* a finite state machine can only transition to a finite (or countable/limited) number of states

# an example

an elevator is a state machine

```mermaid
graph TD
    Ground[Ground Floor] --> |up|First[First Floor]
    First --> |up| Second[Second Floor]
    First --> |down| Ground
    Second --> |down| First
```

# a bigger example

your user account is a state machine

```mermaid
graph TD
    a[anonymous] --> |register| out[logged out]
    out --> |login successfully| l[logged in]
    out --> |fail login|k[locked]
    out --> |fail login| out
    k --> |fail login| disabled
    disabled --> |change password| out
    k --> |change password| out
    l --> |log out| out
    l --> |change password| out
```

You can use a state diagram to communicate and clarify

This is one of the ways that you can make a complicated thing out of little bits of code