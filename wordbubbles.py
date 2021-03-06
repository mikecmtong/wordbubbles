import numpy as np
import sys

class TrieNode:
    def __init__(self):
        self.child = {}     # hash table instead of array[26] since nodes are sparse
        self.word = False   # does a word end on this node

def load_trie():
    s = ord('a')  # shift factor
    dict_file = 'words'
    
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

def search(head, board, lengths, words_found, num_wds):
    lengths = sorted(lengths, reverse=True)  # look for longest length first
    n = len(board)  # assume square dimensions for now
    for i in range(n):
        for j in range(n):   # row then column
            visited = np.zeros([n, n])
            if board[i][j] != -1 and visited[i][j] != 1:
                val = board[i][j]
                words = words_found + [[(chr(val + 97), i, j)]]
                visited[i][j] = 1
                if val in head.child:
                    search_rec(head, head.child[val], board, i, j, visited, words, lengths, num_wds)

def search_rec(head, curr, board, i, j, visited, words, lengths, num_wds):
    word = words[-1]
    if len(word) == lengths[0]:
        if curr.word == True:
            new_board = update_board(board, word)
            if len(lengths) > 1:
                search(head, new_board, lengths[1:], words, num_wds)
            else:
                print "Found a potential solution!"
                for found_word in words:
                    print "%s"%''.join([c[0] for c in found_word]).upper()
                    pretty_print_word(found_word, len(board))
                    sys.stdout.write("\n")
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
                        word += [(chr(val + 97), i+di, j+dj)]
                        visited[i+di][j+dj] = 1
                        search_rec(head, curr.child[val], board, i+di, j+dj, visited, words, lengths, num_wds)
                        visited[i+di][j+dj] = 0
                        word.pop()
                except IndexError:  # at the edge, can't move in that direction
                    continue

def update_board(board, word):
    new_board = np.copy(board)
    for tup in word:
        new_board[tup[1]][tup[2]] = -1
    return new_board

def pretty_print_word(word, n):
    '''prints a found word with the geometry of its actual position in the board
    n: n x n board'''
    pretty_word = np.full([n, n], -1)
    for tup in word:
        pretty_word[tup[1]][tup[2]] = ord(tup[0]) - 97

    for row in pretty_word:
        for elem in row:
            sys.stdout.write("%s "%(chr(int(elem) + 97).upper()))
        sys.stdout.write("\n")

def main():
    if len(sys.argv) > 1:
        print '''        usage:
        - first specify length of words through stdin
        - then give board through stdin, using ` as the empty -1 symbol
        e.g.  3
              f `
              u n
              EOF
        is the first level of wordbubbles.'''
        return 1
    head = load_trie()
    lengths = [int(num) for num in sys.stdin.readline().strip().split(' ')]
    board = []
    for line in sys.stdin:
        line = line.rstrip()
        board.append([ord(c) - ord('a') for c in line.split(' ')])
    board = np.array(board)
    search(head, board, lengths, [], len(lengths))


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
