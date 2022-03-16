## Features
- support custom command prefixes/message prefixes
- add good help messages
- maybe make a macro for parsing args
- decide what errors should be shown
- add counter commands
- add playlist stuff
- add reaction roles stuff (actually probably not but see how hard)
- look into how the cache works more and if I need to care about filling it
- Show ids in `list` commands for deleting quotes


## Refactors

A lot of the commands and client manager structs are very similar. Look into making a trait or macros for implementing them