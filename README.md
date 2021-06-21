# 51AC8
51AC8 is a stack based golfing / esolang that I am trying to make.

**NOTE**: Currently in Development. Things might break.

Issues and PRs welcome.

## Installation
```
git clone https://github.com/Pygamer0/51AC8
```

## Examples
#### Hello, World!
```
ōHello, World!`
```
**or**
```
pHello, World!`
```

#### While loop
```
ī(;ṭ-1)
```
With explanation (another version)
```
ī(     # Take input (int) and start while loop
  ;    # Duplicate the top of the stack
  ³    # Cube the top of the stack
  ±    # Negate the top of the stack
  ½    # Half the top of the stack
  ṭ    # Pop and print
  -1   # Subtract one
)      # End loop
```

