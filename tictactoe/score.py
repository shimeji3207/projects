import shelve, os

'''
# Make a function to ask if the player wants to save their match record.
def save():
    print("成績を記録しますか？(y/n)")
    cmd = input()

    while cmd not in ('y', 'n'):
        print("成績を記録しますか？(y/n)")

    if cmd == 'y':
        shelf_file = shelve.open('record')
        shelf_file['score'] = score
        shelf_file.close()

def load():
    shelf_file = shelve.open('record')
    score = dict(shelf_file['score'])
    shelf_file.close()
    return score
'''