import numpy as np
import sys

class TrieNode:
    def __init__(self):
        self.child = {}     # hash table instead of array[26] since nodes are sparse
        self.word = False   # does a word end on this node

def load_trie():
    s = ord('a')  # shift factor
    dict_file = 'words.txt'
    
    f = open(dict_file, 'r')
    head = TrieNode()
    for line in f:
        curr = head
        line = line.strip().lower()
        for c in line:
            if ord(c) - s not in curr.child:
                curr.child[ord(c) - s] = TrieNode()
            curr = curr.child[ord(c) - s]
        curr.word = True   # end of the word
    return head

def search(head, board, length):
    n = len(board)  # assume square dimensions for now
    for i in range(n):
        for j in range(n):   # row then column
            visited = np.zeros([n, n])
            if board[i][j] != -1:
                val = board[i][j]
                word = [chr(val + 97)]
                visited[i][j] = 1
                if val in head.child:
                    search_rec(head.child[val], board, i, j, visited, word, length)

def search_rec(curr, board, i, j, visited, word, length):
    if len(word) == length:
        if curr.word == True:
            print "Found a word! It's %s"%(''.join(word).upper())
            return
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if i+di != -1 and j + dj != -1:   # have to do this since "-1" indices work in python
                try:
                    if visited[i+di][j+dj] == 1:
                        continue
                    
                    val = board[i+di][j+dj]
                    # condition fails if this block is empty (-1) or leads to no possible words
                    if val in curr.child:   
                        word += [chr(val + 97)]
                        visited[i+di][j+dj] = 1
                        search_rec(curr.child[val], board, i+di, j+dj, visited, word, length)
                        visited[i+di][j+dj] = 0
                        word.pop()
                except IndexError:  # at the edge, can't move in that direction
                    continue

def main():
    '''USAGE:
    Give board through stdin, using ` as the empty -1 symbol
    e.g.  f `\\n
          u n\\n
          EOF
    is the first level of wordbubbles.
    Give length of desired word through argv'''
    head = load_trie()
    board = []
    for line in sys.stdin:
        line = line.rstrip()
        board.append([ord(c) - ord('a') for c in line.split(' ')])
    board = np.array(board)
    print board

    for length in sys.argv[1:]:
        search(head, board, int(length))

    #pretty_print_trie(head)
    #for word in ["amok"]:
    #    is_a_word(head, word)

## TESTING FUNCTIONS ##

def pretty_print_trie(head):
    pp_trie_rec(head, 0, [''])

def pp_trie_rec(curr, depth, word):
    print " "*(depth - 1) + (word[-1].upper() if curr.word else word[-1])
    for i in range(26):
        if i in curr.child:
            word += [chr(i + ord('a'))]
            pp_trie_rec(curr.child[i], depth+1, word)
            word.pop()  # remove character we just added

def is_a_word(head, word):
    '''case sensitive'''
    s = ord('a')  # shift factor
    curr = head
    for c in word:
        if ord(c) - s not in curr.child:
            print "%s is not a word in the trie"%(word)
            return
        curr = curr.child[ord(c) - s]
    if curr.word == True:
        print "%s is a word in the trie"%(word)
    else:
        print "%s is not a word in the trie"%(word)

if __name__ == '__main__':
    main()