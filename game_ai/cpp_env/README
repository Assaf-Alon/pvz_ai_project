# Usage
To compile:
make fast        // Basic
make debug       // Debug mode, extra prints
make clang-debug // Debug mode, extra prints, sanitizer
make fast-sanitize // sanitizer but without debug prints and with extra flags to find rare exceptions
(Then run `./main.out`)
make profile     // Uses gprof to profile the program
`./main.out`
`gprof main.out gmon.out > analysis.txt`

# clang-profile-optimize:
For optimal performance, run `make clang-profile-optimize`.
Note: this will take a while (30-100 sec), but generate code that is up to 2x faster.

# TODO

## Fixes
1. Need to play around with the code to find out more issues

## Enchancements
1. Finish implementing plants (5 left)
2. Think about how to make the random plant generator plant more expensive plants
3. Add random zombie generator?
4. Figure out swig

# 
1. Create function that returns all legal actions for the player (plant, lane, col)