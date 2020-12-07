library(readr)

# This is needed the second you work with strings in R... just
# get rid of some of the annoying fluff. I am not happy with it
# but I couldn't figure out how to work more sanely with it
make_sane <- \(x) x |> unlist(use.names = FALSE)
split <- \(x,s) strsplit(x, split = s) |> make_sane()

# Fixing map/reduce to work with pipelines
map    <- \(x,f)        Map(f,x)           |> make_sane()
reduce <- \(x, f, init) Reduce(f, x, init) |> make_sane()

solve_puzzle <- \(upd, init)
  \(infile) read_file(infile) |> split("\n\n")                      |>
            map(\(group) split(group, '\n')                         |> 
                 reduce(\(acc,ans) upd(acc, split(ans, "")), init)) |>
            map(length) |> sum()

puzzle1 <- solve_puzzle(union, c())
puzzle2 <- solve_puzzle(intersect, split("abcdefghijklmnopqrstuvxyz", ""))

puzzle1('test.txt')
puzzle2('test.txt')

