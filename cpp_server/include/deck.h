#ifndef DECK_H
#define DECK_H

#include <vector>
#include <random>
#include "card.h"

using namespace std;

class Deck
{
public:
    Deck(int num_of_decks);
    ~Deck();

    Card deal_card();
    void shuffle_deck();
    void print_deck();

private:
    mt19937 m_g;
    vector<Card> m_deck;
    int m_length;
};


#endif
