library(tidyverse)

# Separate functions because string handling is a mess in R
split_groups  <- \(x) str_split(x, "\n\n")[[1]]
split_answers <- \(x) str_split(x, "\n")[[1]] |> discard(\(x) x == "")
make_set      <- \(x) str_split(x, "")[[1]]

fname  <- '/Users/mailund/Projects/adventofcode/2020/06/test.txt'
groups <- read_file(fname) |> split_groups()

solve_puzzle <- function(upd) {
  group_answers <- \(x) x |> split_answers() |> map(make_set) |> reduce(upd)
  solve_puzzle  <- \(x) x |> map(group_answers) |> map_dbl(length) |> sum()
  solve_puzzle
}

puzzle1 <- solve_puzzle(union)
puzzle2 <- solve_puzzle(intersect)

puzzle1(groups)
puzzle2(groups)
