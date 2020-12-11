#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

// Code for dealing with maps...
struct map {
    int nrow, ncol;
    char map[];
};
#define IDX(M,I,J)  ((M)->map[(M)->ncol * (I) + (J)])
#define SEAT_OCC(M,I,J) \
    ( ((I) < 0) ? 0 : ((I) >= (M)->nrow) ? 0 : \
      ((J) < 0) ? 0 : ((J) >= (M)->ncol) ? 0 : \
      (IDX(M,I,J) == '#') )
#define FIXPOINT(OLD,NEW) \
    (!memcmp((OLD)->map, (NEW)->map, (OLD)->nrow * (OLD)->ncol))

static struct map *new_map(int nrow, int ncol)
{
    struct map *map = malloc(offsetof(struct map, map) + nrow * ncol);
    if (map) { map->nrow = nrow; map->ncol = ncol; }
    return map;
}
static struct map *clone_map(struct map *map)
{
    struct map *clone = new_map(map->nrow, map->ncol);
    memcpy(clone->map, map->map, map->nrow * map->ncol);
    return clone;
}

static inline
int count_occupied(struct map *map)
{
    int n = map->nrow * map->ncol;
    int count = 0;
    for (char *x = map->map; x < map->map + n; x++)
        count += (*x == '#');
    return count;
}


// Generic code for evolving a map
typedef char (*local_upd)(struct map *map, int i, int j, char old);
static void update_map(struct map *new_map, struct map *old_map, local_upd upd)
{
    char *x = new_map->map, *y = old_map->map;
    for (int i = 0; i < new_map->nrow; i++) {
        for (int j = 0; j < new_map->ncol; j++)
            *x++ = upd(old_map, i, j, *y++);
    }
}

static void evolve(struct map *input_map, local_upd upd)
{
    struct map *helper = clone_map(input_map);
    struct map *maps[] = { input_map, helper };
    int cur_map = 0;
    do {
        update_map(maps[(cur_map + 1) % 2], maps[cur_map % 2], upd);
        cur_map++;
    } while (!FIXPOINT(maps[0], maps[1]));
    free(helper);
}




// Puzzle 1 ---------------------------------------------------
static inline
int count_adjecant(struct map *map, int i, int j)
{
    int count = 0;
    for (int k = -1; k <= 1; k++) {
        for (int l = -1; l <= 1; l++)
            // branching-less condition
            count += (k != 0 || l != 0) * SEAT_OCC(map, i+k, j+l);
    }
    return count;
}

static inline
char update_seat_puzzle1(struct map *map, int i, int j, char old_seat)
{
    if (old_seat == '.')                              return old_seat;
    int occ_count = count_adjecant(map, i, j);
    if      (old_seat == 'L' && occ_count == 0)       return '#';
    else if (old_seat == '#' && occ_count >= 4)       return 'L';
    else                                              return old_seat;
}

static int puzzle1(struct map *map)
{
    evolve(map, update_seat_puzzle1);
    return count_occupied(map);
}

// Puzzle 2 ---------------------------------------------------
static inline 
int seat_direction(struct map *map, int i, int j, int di, int dj)
{
    if (di == 0 && dj == 0) return 0; // easier to test this here
    int n = map->nrow, m = map->ncol;
    i += di; j += dj;
    while (i >= 0 && i < n && j >= 0 && j < m) {
        char seat = IDX(map,i,j);
        if (seat == '#') return 1;
        if (seat == 'L') return 0;
        i += di; j += dj;
    }
    return 0;
}

static inline
int count_neighbours(struct map *map, int i, int j)
{
    int count = 0;
    for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++)
            count += seat_direction(map, i, j, di, dj);
    }
    return count;
}

static inline
char update_seat_puzzle2(struct map *map, int i, int j, char old_seat)
{
    if (old_seat == '.')                              return old_seat;
    int occ_count = count_neighbours(map, i, j);
    if      (old_seat == 'L' && occ_count == 0)       return '#';
    else if (old_seat == '#' && occ_count >= 5)       return 'L';
    else                                              return old_seat;
}

static int puzzle2(struct map *map)
{
    evolve(map, update_seat_puzzle2);
    return count_occupied(map);
}


void print_map(struct map *map)
{
    printf("\n%d x %d map:\n", map->nrow, map->ncol);
    for (int i = 0; i < map->nrow; i++) {
        for (int j = 0; j < map->ncol; j++) {
            putchar(map->map[map->ncol * i + j]);
        }
        putchar('\n');
    }
    putchar('\n');
}


// only for IO. Not pretty, but don't care
#define N 1000
char input_buf[N];
static struct map *read_map(void)
{
    // getting too much memory for the initial map, but who cares?
    struct map *map = new_map(N, N);
    fgets(input_buf, N, stdin);
    int ncol = strlen(input_buf) - 1;
    int nrow = 0;
    memcpy(map->map + nrow++ * ncol, input_buf, ncol);
    while (fgets(input_buf, N, stdin)) {
        memcpy(map->map + nrow++ * ncol, input_buf, ncol);
    }
    // getting the correct dimensions
    map->nrow = nrow; map->ncol = ncol;
    return map;
}


int main(void)
{
    struct map *map = read_map();
    struct map *puzzle1_clone = clone_map(map);
    printf("Puzzle #1: %d\n", puzzle1(puzzle1_clone));
    free(puzzle1_clone);

    printf("Puzzle #2: %d\n", puzzle2(map));
    free(map);

    return 0;
}
