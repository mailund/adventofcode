#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>

// Linked list -----------------------------------------
struct link {
  int value;
  struct link *prev;
  struct link *next;
};

struct link *new_link(int val)
{
  struct link *link = malloc(sizeof *link);
  if (!link) abort();
  link->value = val;
  link->prev = link->next = 0;
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
#define front(x)    (head(x)->next)
#define back(x)     (head(x)->prev)
#define is_empty(x) ( head(x) == front(x) )
#define length(x)   ((x)->len)

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


void append(struct list *x, struct link *link)
{
    link_after(back(x), link);
    x->len++;
}

struct link *pop_front(struct list *x)
{
    assert(!is_empty(x));
    struct link *link = front(x);
    unlink(link); x->len--;
    return link;
}

struct list *make_list(int n, int array[n])
{
    struct list *x = new_list();
    for (int i = 0; i < n; i++) {
        append(x, new_link(array[i]));
    }
    return x;
}

struct list *copy_prefix(struct list *x, int n)
{
    struct list *copy = new_list();
    struct link *link = front(x);
    while (link != head(x) && n) {
        append(copy, new_link(link->value));
        link = link->next;
        n--;
    }
    return copy;
}
#define copy_list(x) copy_prefix(x, length(x))


int compare_lists(struct list *x, struct list *y)
{
    struct link *lx = front(x);
    struct link *ly = front(y);
    while (lx != head(x) && ly != head(y)) {
        if (lx->value != ly->value) return lx->value - ly->value;
        lx = lx->next; ly = ly->next;
    }
    // maybe they are equal?
    if (lx == head(x) && ly == head(y)) return 0;
    // One is a prefix of another -- the shorter is the smallest
    return (lx == head(x)) ? -1 : 1;
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

// Search tree -----------------------------------------
struct node {
  struct list *value;
  struct node *left;
  struct node *right;
};

struct node *node(struct list *value, 
                  struct node *left, struct node *right)
{
  struct node *t = malloc(sizeof *t);
  if (!t) abort();
  *t = (struct node){
    .value = copy_list(value), 
    .left = left, .right = right
  };
  return t;
}
#define leaf(V) node(V, 0, 0)

// tail recursive
bool contains(struct node *t, struct list *x)
{
  if (!t) return false;
  int cmp = compare_lists(x, t->value);
  if (cmp == 0) return true;
  if (cmp < 0)  return contains(t->left, x);
  else          return contains(t->right, x);
}


struct node *insert_node(struct node *t, struct node *n)
{
  if (!t) return n;
  int cmp = compare_lists(n->value, t->value);
  if (cmp == 0) {
    free(n); // it was already here
  } else if (cmp < 0) {
    t->left = insert_node(t->left, n);
  } else {
    t->right = insert_node(t->right, n);
  }
  return t;
}

struct node *insert(struct node *t, struct list *x)
{
  struct node *n = leaf(x);
  if (!n) return 0;
  return insert_node(t, n);
}

void print_stree(struct node *t)
{
  if (!t) return;
  putchar('(');
    print_stree(t->left);
    putchar(',');putchar('[');
    print_list(t->value);
    putchar(']');putchar(',');
    print_stree(t->right);
  putchar(')');
}

// Not tail recursive
void free_stree(struct node *t)
{
  if (!t) return;
  free_stree(t->left);
  free_stree(t->right);
  free_list(t->value);
  free(t);
}


// Games -----------------------------------------------

struct list *play(struct list *p1, struct list *p2)
{
    while (!is_empty(p1) && !is_empty(p2)) {
        struct link *card1 = pop_front(p1);
        struct link *card2 = pop_front(p2);
        if (card1->value > card2->value) {
            append(p1, card1); append(p1, card2);
        } else {
            append(p2, card2); append(p2, card1);
        }
    }
    return is_empty(p1) ? p2 : p1;
}

struct game2_res {
    int winner;
    struct list *winner_hand;
};
#define WIN(w,wh) \
    (struct game2_res){ .winner = (w), .winner_hand = (wh) }

struct game2_res play2(struct list *p1, struct list *p2)
                       
{
    struct node *s1 = 0;
    struct node *s2 = 0;
    struct game2_res winner;

    while (!is_empty(p1) && !is_empty(p2)) {
        if (contains(s1, p1) || contains(s2, p2)) {
            winner = WIN(1, p1);
            goto finish;
        }
        s1 = insert(s1, p1);
        s2 = insert(s2, p2);

        struct link *card1 = pop_front(p1);
        struct link *card2 = pop_front(p2);
        int w;
        if (card1->value > length(p1) || card2->value > length(p2)) {
            w = (card1->value > card2->value) ? 1 : 2;
        } else {
            struct game2_res rec_res;
            struct list *p1_copy = copy_prefix(p1, card1->value);
            struct list *p2_copy = copy_prefix(p2, card2->value);
            rec_res = play2(p1_copy, p2_copy);
            w = rec_res.winner;
            free_list(p1_copy);
            free_list(p2_copy);
        }

        if (w == 1) {
            append(p1, card1); append(p1, card2);
        } else {
            append(p2, card2); append(p2, card1);
        }
    }


    winner = is_empty(p1) ? WIN(2,p2) : WIN(1,p1);
finish:
    free_stree(s1);
    free_stree(s2);
    return winner;
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

void puzzle1(struct list *p1, struct list *p2)
{
    struct list *p1c = copy_list(p1);
    struct list *p2c = copy_list(p2);
    
    struct list *winner = play(p1c, p2c);
    printf("Score: %d\n", hand_score(winner));
    
    free_list(p1c);
    free_list(p2c);
    // winner is a copy of one of them, so it should not
    // be freed.
}

void puzzle2(struct list *p1, struct list *p2)
{
    struct list *p1c = copy_list(p1);
    struct list *p2c = copy_list(p2);
    
    struct game2_res res = play2(p1c, p2c);
    printf("Score: %d\n", hand_score(res.winner_hand));
    
    free_list(p1c);
    free_list(p2c);
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

    puzzle1(p1, p2);
    puzzle2(p1, p2);

    free_list(p1);
    free_list(p2);

    return 0;
}