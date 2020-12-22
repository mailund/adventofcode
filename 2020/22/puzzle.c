#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct link {
  int value;
  struct link *prev;
  struct link *next;
};

struct link *
new_link(int val, struct link *prev, struct link *next)
{
  struct link *link = malloc(sizeof *link);
  if (!link) abort();

  link->value = val;
  link->prev = prev;
  link->next = next;
  return link;
}

static inline
void connect_neighbours(struct link *x)
{ x->next->prev = x; x->prev->next = x; }

static inline
void link_after(struct link *x, struct link *y)
{ y->prev = x; y->next = x->next; connect_neighbours(y); }

static inline
void unlink(struct link *x)
{ x->next->prev = x->prev; x->prev->next = x->next; }



struct list {
    int len;
    struct link head;
};

#define head(x)     (&((x)->head))
#define front(x)    head(x)->next
#define back(x)     head(x)->prev
#define is_empty(x) ( head(x) == front(x) )
#define length(x)   (x)->len

struct list *new_list(void)
{
    struct list *x = malloc(sizeof *x);
    if (!x) abort();
    x->head.next = x->head.prev = &x->head;
    x->len = 0;
    return x;
}

void free_list(struct list *x)
{
    struct link *link = front(x);
    while (link != head(x)) {
        struct link *next = link->next;
        free(link);
        link = next;
    }
    free(x);
}

void append(struct list *x, int val)
{
    struct link *link = new_link(val, back(x), head(x));
    connect_neighbours(link);
}

int pop_front(struct list *x)
{
    assert(!is_empty(x));
    struct link *link = front(x);
    int retval = link->value;
    unlink(link); free(link);
    return retval;
}

struct list *make_list(int n, int array[n])
{
    struct list *x = new_list();
    for (int i = 0; i < n; i++) {
        append(x, array[i]);
    }
    return x;
}

static void
print_list(struct list *x)
{
    struct link *link = front(x);
    while (link != &x->head) {
        printf("%d ", link->value);
        link = link->next;
    }
    printf("\n");
}

struct list *play(struct list *p1, struct list *p2)
{
    while (!is_empty(p1) && !is_empty(p2)) {
        int card1 = pop_front(p1);
        int card2 = pop_front(p2);
        if (card1 > card2) {
            append(p1, card1); append(p1, card2);
        } else {
            append(p2, card2); append(p2, card1);
        }
    }
    return is_empty(p1) ? p2 : p1;
}

int hand_score(struct list *hand)
{
    int res = 0;
    int multiple = 1;
    struct link *link = back(hand);
    while (link != head(hand)) {
        res += multiple * link->value;
        multiple += 1;
        link = link->prev;
    }
    return res;
}

int main(void)
{
    // Parsing the input left as an exercise for the reader...
    int p1_input[] = { 9, 2, 6, 3,  1 };
    int p2_input[] = { 5, 8, 4, 7, 10 };

    struct list *p1 = make_list(sizeof p1_input / sizeof *p1_input, p1_input);
    struct list *p2 = make_list(sizeof p2_input / sizeof *p2_input, p2_input);

    print_list(p1);
    print_list(p2);

    struct list *winner = play(p1, p2);
    print_list(winner);
    printf("Score: %d\n", hand_score(winner));

    return 0;
}