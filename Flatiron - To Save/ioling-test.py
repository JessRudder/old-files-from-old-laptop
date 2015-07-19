import re
from nltk.util import ngrams

def english_sentences (word_list):
    '''
    Takes a list of English sentences broken into words, then determines the frequency count and location of each word within the list.
    Uses a fuzzy definition of word closer to "lexical item".

    Example:
    english_sentences( (('I', 'am', 'not', 'happy') , ('You', 'are', 'very', 'very', 'happy')) )   =>     [['happy', [0, 1]], ['very', [1, 1]]]
        
    inputs:
        word_list <- a list of sublists. Each sublist should be a full English phrase or sentence broken into words.
    builds:
        word_dict <- a dictionary with:
            KEYS <- every lexical item that occurs in the English text
            VALUES <- (num_occurrences , (index_1, index_2 ... index_n) ) where index_n is the sentence number location of each occurrence
            NOTE that a single index can be listed multiple times, as indices is added whenever a word occurs (even within a single sentence).
    returns:
        example_map <- a list out of word_dict where each item that occurs more than once has the following mapping:
            [ key occuring > 1 times , [ index_1, index_2 ... index_n ]
            NOTE that a single index can be listed multiple times, as indices is added whenever a word occurs (even within a single sentence).
            NOTE that the bottom branch currently gets rid of common little words like determiners
    facilitates:
        comparing word_dict to a similar dictionary in a candidate language for coherence patterns among the index numbers to guess at translations
    '''
    
    word_dict = {}      # will be used to associate occurrences of words with when and where they occur in text

    # use the word list to go thru the example sentences, look for occurrences & put those occurrences in word_dict
    # grab each word from our list
    for sentence in word_list:
        for word in sentence:
            # NEW WORD FOUND: add dict entry for this frequency and index
            if word not in word_dict:
                word_dict[word] = [1, [word_list.index(sentence)] ]
            # ANOTHER INSTANCE FOUND: augment dict entry for this frequency and index
            elif word in word_dict:
                # increase the frequency count by 1
                word_dict[word][0] += 1
                # list the index of the sentence in which the word occurs
                word_dict[word][1].append(word_list.index(sentence))

            # FUZZY MATCH TEST: add the stem of words that contain common suffixes
            # 
            if len(word) > 3:
            # filter for longer words to avoid overmatching
                # check if the last letter is a suffix
                if word[len(word)-1:len(word)] in ('s', 'd'):
                    stem = word[:len(word)-1]
                    # increase count and index if it's already in the dict
                    if stem in word_dict:
                        word_dict[stem][0] += 1
                        word_dict[stem][1].append (word_list.index(sentence))
                    # add stem if it's not in dict
                    else:
                        word_dict[stem] = [1 , [word_list.index(sentence)] ]
                # check if the last two letters are a suffix
                if word[len(word)-2:len(word)] in ('es', 'ed', 'er'):
                    stem = word[:len(word)-2]
                    # check to see if last 2 chars of stem are geminate; if so, cut the stem shorter 
                    if stem[len(stem)-2] == stem[len(stem)-1]:
                        stem_short = stem[:len(stem)-1]
                        if stem_short in word_dict:
                            word_dict[stem_short][0] += 1
                            word_dict[stem_short][1].append (word_list.index(sentence))
                        # add stem if it's not in dict
                        else:
                            word_dict[stem_short] = [1 , [word_list.index(sentence)] ]
                    # increase count and index of the stem if it's already in the dict
                    if stem in word_dict:
                        word_dict[stem][0] += 1
                        word_dict[stem][1].append (word_list.index(sentence))
                    # add stem if it's not in dict
                    else:
                        word_dict[stem] = [1 , [word_list.index(sentence)] ]
                # check if the last three letters are a suffix
                elif word[len(word)-3:len(word)] in ('ing', 'ers', 'est'):
                    stem = word[:len(word)-3]
                    # check to see if last 2 chars of stem are geminate; if so, cut the stem shorter 
                    if stem[len(stem)-2] == stem[len(stem)-1]:
                        stem_short = stem[:len(stem)-1]
                        if stem_short in word_dict:
                            word_dict[stem_short][0] += 1
                            word_dict[stem_short][1].append (word_list.index(sentence))
                        # add stem if it's not in dict
                        else:
                            word_dict[stem_short] = [1 , [word_list.index(sentence)] ]
                    # increase count and index of the stem if it's already in the dict
                    if stem in word_dict:
                        word_dict[stem][0] += 1
                        word_dict[stem][1].append (word_list.index(sentence))
                    # add stem if it's not in dict
                    else:
                        word_dict[stem] = [1 , [word_list.index(sentence)] ]
                else:
                    pass
            
    # create a list in which all found words and locations will be stored
    example_map = []
    # add to list only words that occur more than once, along with their locations
    for k in word_dict:
        # get rid of common little words for easier comparison
        if k not in ('the', 'a', 'an', 'if', 'for', 'of', 'to', 'at'):
            if word_dict[k][0] > 1:
                example = [k , word_dict[k][1] ]
                example_map.append(example)

    # return only the numbers in the example map, unweighted by frequency occurrence
    return_vals = []
    for i in range (0, len(example_map) ):
    # iterate through results, dig out only occurrence locations, put them in new list with no dups
        if example_map[i][1] not in return_vals:
            return_vals.append(example_map[i][1])
            
    return return_vals


def puzzle_sentences (word_list):
    '''
    Takes a list of unknown sentences. Determines if any of their grams show up anywhere else in the sentences. Returns a list
    of all the examples of multiple matches, including which sentences they occur in.

    Example:
    puzzle_sentences( (('zzxzzz gyyyggr') , ('zzz yyyyxyg')) )   =>     [['zzz', [0, 1]], ['yyyy', [0, 1]]]
        
    inputs:
        word_list <- a list of sublists and subsublists. Each sublist should be a full phrase or sentence broken into words, while each subsublist is ngrams of those words.
    builds:
        word_dict <- a dictionary with:
            KEYS <- every ngram that occurs in the text
            VALUES <- (num_occurrences , (index_1, index_2 ... index_n) ) where index_n is the sentence number location of each occurrence
    returns:
        example_map <- a list out of word_dict where each item that occurs more than once has the following mapping:
            [ key occuring > 1 times , [ index_1, index_2 ... index_n ]
            NOTE that a single index can be listed multiple times, as indices is added whenever a word occurs (even within a single sentence).
    facilitates:
        comparing word_dict to a similar dictionary in a candidate language for coherence patterns among the index numbers to guess at translations
    '''
    
    word_dict = {}      # will be used to associate occurrences of words with when and where they occur in text

    # use the word list to go thru the example sentences, look for occurrences & put those occurrences in word_dict
    # grab each word from our list
    for sentence in word_list:
        for word in sentence:
            for gram in word:
            
                # NEW MATCH FOUND: add dict entry for this frequency and index
                if gram not in word_dict:
                    word_dict[gram] = [1, [word_list.index(sentence)] ]
            
                # ANOTHER INSTANCE FOUND: augment dict entry for this frequency and index
                elif gram in word_dict:
                    # increase the frequency count by 1
                    word_dict[gram][0] += 1
                    # list the index of the sentence in which the word occurs
                    word_dict[gram][1].append(word_list.index(sentence))

    # create a list in which all matched ngrams will be stored
    example_map = []
    # add to list only ngrams that occur more than once, along with locations
    for k in word_dict:
        if word_dict[k][0] > 1:
            example = [k , word_dict[k][1] ]
            example_map.append(example)

    # clean up examples by removing substrings with the same list of sentence occurrences
    # create a list for all the words
##    temp_list = []
##    # create a list that we can change while iterating thru example_map
##    new_example_map = []
##    # populate our two lists from example_map
##    for entry in example_map:
##        temp_list.append(entry[0])
##        new_example_map.append(entry)
##    # check all examples against each other
##    for i in temp_list:
##        for j in example_map:
##            # remove submatching ngrams if one is a substring of the other and they both occur in the same sentences
##            if j[0] in i and len(j[0]) < len(i) and j[1] == example_map[temp_list.index(i)][1]:
##                if [j[0],j[1]] in new_example_map:
##                # take it from the new list (so you don't mess up the loop) but only try if it's in the new list (otherwise error)
##                    new_example_map.remove([j[0],j[1]])

    # return only the numbers in the example map, unweighted by frequency occurrence
    return_vals = []
    for i in range (0, len(example_map) ):
    # iterate through results, dig out only occurrence locations, put them in new list with no dups
        if example_map[i][1] not in return_vals:
            return_vals.append(example_map[i][1])

    return return_vals


def parse_words (sentence_list):
    '''
    Takes a list of sentences and turns it into a list of wordlists.

    Example:
    parse_words( ('I am happy.' , 'You are happy!') )   =>      ( ('i', 'am', 'happy') , ('you', 'are', 'happy') )
    
    inputs:
        sentence_list <- a list of sentences
    outputs:
        word_list <- a list of lists, where each sublist separates out all words in the original sentence at that same index in sentence_list

    facilitates:
        counting the occurrence location and frequency of words within each sentence
    '''
    # create a new list to store lists of sentences, broken into words
    word_list = []

    # chop up each sentence into a list of words using regex
    for s in sentence_list:
        # create a temporary tuple of words and a permanent list where filtered words will be stored
        temp_words = re.split ('\W+', s)
        words_in_s = []
        # determine and store the sentence's punctuation mark
        #if '.' in s:
        #    punct = '.'
        #elif '!' in s:
        #    punct = '!'            
        #elif '?' in s:
        #    punct = '?'
        #else:
        #    pass
        # take the temporary list of words and add each, uncapsed, to the permanent list
        for w in temp_words:
            # only add the word to the new permanent list if it's not empty ''
            if w != '':
                words_in_s.append(w.lower())
        ## add the sentence's punctuation mark to the list
        #words_in_s.append(punct)
        # add the permanent list to the total word_list (the list of all sentences, broken into words)
        word_list.append(words_in_s)
        
    return word_list

def parse_ngrams (word_list, gram_length=3):
    '''
    Takes a list of sentences broken into words and turns it into a list of sentences broken into words broken into ngrams.

    Example:
    parse_words( (('i', 'know') , ('you', 'know')) , 3)   =>   ( (('kno', 'now', 'know')) , (('you') , ('kno', 'now', 'know')) )
    
    inputs:
        word_list   <- a list of lists, where each sublist contains all of the words in a sentence
        gram_length <- the MIN length of ngrams to search for within each word
        NOTE output will not include anything shorter than the user declared ngram length!
        
    outputs:
        ngram_list <- a list of list of lists, where
            each list item is a sentence
            each sublist item is a word
            each subsublist item is a list of ngrams of that word

    facilitates:
        counting the occurrence location and frequency of ngrams within each sentence
    '''
    # create a new list to store lists of sentences, broken into ngrams
    ngram_list = []

    # chop up each sentence into a list of ngrams of all reasonable lengths using NLTK.util ngrams (imported at top of this py)
    for s in word_list:
    # drill down into the sentences
        this_sentence = []
        for w in s:
        # drill down to the words in the sentence
            this_word = []
            for i in range (gram_length, len(w)):
            # break the word down into all ngrams between user's gram_length and the word's length                
                for j in ngrams(w,i):
                    # ngrams returns a tuple; make entries into strings
                    this_gram = ''
                    for char in j:
                        this_gram += char
                    # add each string into a list for each word
                    this_word.append(this_gram)
            # if the word's not empty, add this word into a list for each sentence
            if this_word != []:
                this_sentence.append(this_word)
        # add each sentence back into the total list
        ngram_list.append(this_sentence)

    return ngram_list

def deg_separ_matcher (loc_list):
    '''
    Takes a list of lists of occurrence locations searches it for degree-of-separation patterns (do numbers that occur with numbers that occur with me also occur with me?).
        
    inputs:
        loc_list    <-  a list of sublists, where each sublist is a collection of locations where a word/ngram match was found
    outputs:
        decision    <-  a dictionary mapping to a decision tree, where each
                        KEY     is the number under consideration in a location list, and
                        VALUE   is a list of n-branch depth searches for numbers that occur in any list with the previous branching number, along with Y or N for whether that number also occurs in any list with the original KEY number

            e.g. traversing [[0,1,3],[0,2,4]], looking at the key 1:

                          1            1
                         / \          / \
                        0   3        Y   Y
                       / \          / \
                      2   4        N  N

                    yields the entry    1: [[Y,Y],[N,N]]

    facilitates:
        matching patterns between distinct sets of numbers, where the pattern of cooccurrences has strict logical coherence, but the mapping between numbers is unknown
    '''

    pattern_dict = {}

    # create a basic dictionary associating each num with other nums that occur in same list at any point
    for locations in loc_list:
    # drill into list of nums
        for loc in locations:
        # drill down to nums themselves
            # create a list of locations that cooccur with loc
            if loc not in pattern_dict:
            # new dictionary entry if num isn't already a key
                pattern_dict[loc] = []
            for loc2 in locations:
            # add nums that aren't already in that value and that aren't identical to the key (keys always occur with themselves in a list!)
                if loc2 != loc and loc2 not in pattern_dict[loc]:
                    pattern_dict[loc].append (loc2)

    # take pattern dictionary above and branch patterns based on degree of separation of cooccurrences
    solutions_dict = {}
    for loc in pattern_dict:
        lvl_1 = []
        lvl_2 = []
        lvl_3 = []
        # dig into the first branch. All these cooccur with loc, so pass Y for each
        for coloc in pattern_dict[loc]:
            lvl_1.append('Y')
            lvl_1.append(coloc)
            #dig into the 2nd branch. Check if the number in question occurs within the coloc's list
            for sub_coloc in pattern_dict[coloc]:
                # is the original num in the list of nums that occur (sub_colocs) with the nums that occur (colocs) with the original num?
                if loc in pattern_dict[sub_coloc] and sub_coloc not in lvl_1:
                    lvl_2.append('Y')
                    lvl_2.append(sub_coloc)
                elif loc not in pattern_dict[sub_coloc] and sub_coloc not in lvl_1:
                    lvl_2.append('N')
                    lvl_2.append(sub_coloc)
                else:
                    pass
                #dig into the 3rd branch. Check if the number in question occurs within the sub_coloc's list
                for sub_sub_coloc in pattern_dict[sub_coloc]:
                # is the original num in the list of nums that occur (sub_sub_colocs) with the numbs that cooccur (sub_colocs) with the nums that cooccur (colocs) with the original num?                    
                    if loc in pattern_dict[sub_sub_coloc] and sub_sub_coloc not in lvl_2:
                        lvl_3.append('Y')
                    elif loc not in pattern_dict[sub_sub_coloc] and sub_sub_coloc not in lvl_2:
                        lvl_3.append('N')
                    else:
                        pass
        # add loc's first list to total list
        total = [lvl_1, lvl_2, lvl_3]
        solutions_dict[loc] = total
        
    return solutions_dict

## write funct that compares 2 dictionaries to determine which keys have the same values, and pair those keys
def dict_compar (d1, d2):
    matches = []
    for k1, v1 in d1.iteritems():
        for k2, v2 in d2.iteritems():
            if v1[0].count('Y') == v2[0].count('Y') and v1[0].count('N') == v2[0].count('N'):
                if v1[1].count('Y') == v2[1].count('Y') and v1[1].count('N') == v2[1].count('N'):
                    if v1[2].count('Y') == v2[2].count('Y') and v1[2].count('N') == v2[2].count('N'):
                        matches.append ([k1, k2])
    return matches

agk_prob_en = ['the donkey of the master', 'the brothers of the merchant', 'the merchants of the donkeys', 'the sons of the masters', 'the slave of the sons', 'the masters of the slaves', 'the house of the brothers', 'the master of the house']
agk_prob_agk = ['ho ton hyion dulos', 'hoi ton dulon cyrioi', 'hoi tu emporu adelphoi', 'hoi ton onon emporoi', 'ho tu cyriu onos', 'ho tu oicu cyrios', 'ho ton adelphon oicos', 'hoi ton cyrion hyioi']

tgt_list = agk_prob_en
tgt_list = parse_words (tgt_list)
tgt_list = english_sentences(tgt_list)
#tgt_list = parse_ngrams(parse_words (tgt_list))
#print puzzle_sentences(tgt_list)

src_list = agk_prob_agk
src_list = parse_ngrams(parse_words (src_list))
src_list = puzzle_sentences(src_list)

src_dict = deg_separ_matcher(src_list)
tgt_dict = deg_separ_matcher(tgt_list)
print src_dict
print tgt_dict
print dict_compar(src_dict, tgt_dict)
