

def main():
    book_name = None

    while book_name is None:
        book_name = input("Enter the name of the book: ") 
    
    book_name += ".txt"

    try:
        book_contents = open_book(book_name)
    except Exception as e:
        print("could not find book.")

    top_line = f"=========== {book_name} ==========="
    bottom_line = ""
    for i in top_line:
        bottom_line += "="

    print(f"{top_line}")
    print("Word count: ")
    print(count_words(book_contents))
    print("\n")
    print("Letter counts: ")
    print(count_letters(book_contents))
    print("\n")
    print(f"{bottom_line}")


def open_book(book_name):
    book = ""
    print(f"Opening {book_name}...")
    with open(f"books/{book_name}") as f:
        book = f.read()
    
    return book 

def count_words(book): 
    words = book.split()
    return len(words)

def sort_on(d):
    return d["num"]

def count_letters(book):
    letter_count = {}
     
    book = book.lower()

    for i in book:
        if i in letter_count:
            letter_count[i] += 1
        else:
            if not i.isalpha():
                continue
            letter_count[i] = 1
    
    sorted_list = []

    for i in letter_count:
        sorted_list.append({"char": i, "num": letter_count[i]})
    
     
    sorted_list.sort(key=sort_on, reverse=True)

    display = ""

    for i in sorted_list:
        display += f"The '{i["char"]}' character was found {i["num"]} times"
        display += "\n"
    
    return display


main()
