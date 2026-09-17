# -----------Import Modules-----------
import sqlite3


# -------------Functions--------------
# Database Related Functions
def get_db_connection():
    '''establish db connection to ebookstore.db'''
    return sqlite3.connect('ebookstore.db')


def create_btable(cursor, edb):
    '''Creates book table, add data to table '''
    try:
        # create table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authorID INTEGER NOT NULL,
            qty INTEGER NOT NULL)'''
        )

        # add info to table
        book_info = [
            (3001, 'A Tale of Two Cities', 1290, 30),
            (3002, 'Harry Potter and the Philosopher\'s Stone', 8937, 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
            (3004, 'The Lord of the Rings', 6380, 37),
            (3005, 'Alice\'s Adventures in Wonderland', 5620, 12)
        ]

        cursor.executemany(
            '''
            INSERT OR IGNORE INTO book(id, title, authorID, qty)
            VALUES (?, ?, ?, ?)''', book_info
        )

        # commit changes to database
        edb.commit()
    except sqlite3.Error:
        edb.rollback()
        print('Book table creation unsuccessful!')


def create_atable(cursor, edb):
    '''Create author table, add data to table'''
    try:
        # create table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL)'''
        )

        # add info to table
        author_info = [
            (1290, 'Charles Dickens', 'England'),
            (8937, 'J.K. Rowling', 'England'),
            (2356, 'C.S. Lewis', 'Ireland'),
            (6380, 'J.R.R. Tolkien', 'South Africa'),
            (5620, 'Lewis Carroll', 'England')
        ]

        cursor.executemany(
            '''
            INSERT OR IGNORE INTO author(id, name, country)
            VALUES (?, ?, ?)''', author_info
        )

        # commit changes to database
        edb.commit()
    except sqlite3.Error:
        edb.rollback()
        print('Author table creation unsuccessful!')


# Helper Functions
def get_book_id(cursor):
    '''Prints book list from database, asks user for book id,
    returns a valid book id'''
    # print book list and make list of book ids
    cursor.execute('''SELECT id, title FROM book''')
    book_info = cursor.fetchall()
    book_id_list = []
    print("\nBook List:")
    for book in book_info:
        print(f'{book[0]}: {book[1]}')
        book_id_list.append(book[0])
    # get input from user for id
    while True:
        try:
            b_id = int(input("Please enter the id of the book "
                             "for the respective task: "))
            if len(str(b_id)) == 4:
                if b_id in book_id_list:
                    return b_id
                else:
                    print("Invalid book id. Refer to book list above!")
            else:
                print("Book id can only be 4 integers")
        except ValueError:
            print("Invalid input! Enter a 4 integer book id.")


def get_author_id(cursor):
    '''Prints author list from database, ask user for author is,
    returns valid author id'''
    cursor.execute('''SELECT id, name FROM author''')
    author_info = cursor.fetchall()
    author_id_list = []
    print("\nAuthors:")
    for author in author_info:
        print(f'{author[0]}: {author[1]}')
        author_id_list.append(author[0])
    while True:
        try:
            b_author_id = int(input("\nPlease enter the new book author "
                                    "id from the list above: "))
            if len(str(b_author_id)) == 4:
                if b_author_id in author_id_list:
                    return b_author_id
                else:
                    print("Invalid input! Refer to author list above.")
            else:
                print("Author id can only be 4 integers.")
        except ValueError:
            print("Invalid input! Please enter 4 integer author id")


def get_or_add_author(cursor, edb):
    '''Lists authors, gets a valid author id from user or adds
    a new author to database, returns the author id'''
    cursor.execute("SELECT id, name FROM author")
    author_ids_tuple = cursor.fetchall()
    a_list = []
    print("\nAuthor List")
    for row in author_ids_tuple:
        print(f'{row[0]}: {row[1]}')
        a_list.append(row[0])
    # ask user if author for new book is listed or not
    while True:
        choice = input('''\n
Is the author for the new book already listed above:
1: Yes
2: No - I need to register a new author
Enter choice: ''')
        if choice in ["1", "2"]:
            break
        else:
            print("Invalid input! Try again!")
    if choice == "1":
        while True:
            try:
                b_author_id = int(input("Please enter the book author id: "))
                if len(str(b_author_id)) == 4:
                    if b_author_id in a_list:
                        return b_author_id
                    else:
                        print("Invalid input! Refer to author list above,")
                else:
                    print("Author id can only be 4 integers.")
            except ValueError:
                print("Invalid input! Please enter 4 integer author id.")
    elif choice == "2":
        print("To enter a new author please enter the following information:")
        while True:
            try:
                new_a_id = int(input("Please input the author id "
                                     "(4 integers): "))
                if new_a_id in a_list:
                    print("Author id taken! Try again!")
                elif len(str(new_a_id)) == 4:
                    new_a_name = input("Please enter the author's full name: ")
                    new_a_country = input("Please enter the country where "
                                          "the author is from: ")
                    try:
                        cursor.execute('''
                                       INSERT INTO author(id, name, country)
                                       VALUES (?, ?, ?)''',
                                       (new_a_id, new_a_name, new_a_country))
                        # commit changes to database
                        print("New author added!")
                        edb.commit()
                    except sqlite3.Error:
                        edb.rollback()
                        print('Author addition unsuccessful!')
                    return new_a_id
                else:
                    print("Invalid input - ensure 4 digits entered for id")
            except ValueError:
                print("Invalid input - enter 4 integers for the id")

    else:
        print("Invalid input! Try again")


def update_qty(cursor, edb, update_b_id):
    '''Ask user for new quantity for a specific book,
    update to database'''
    print("\nUpdating book quantity:")
    # get valid quantity
    while True:
        try:
            new_qty = int(input("Enter the new book quantity: "))
            if new_qty >= 0:
                break
            else:
                print("Quantity cannot be negative. Try again!")
        except ValueError:
            print("Invalid input. Try again!")
    # update info in database
    try:
        cursor.execute('''
                       UPDATE book SET qty = ? WHERE id = ?''',
                       (new_qty, update_b_id))
        edb.commit()
        print("Book quantity successfully updated!")
    except sqlite3.Error:
        print("Update unsuccessful. Try again")
        edb.rollback()


def update_title(cursor, edb, update_b_id):
    '''Ask user for updated title for a specific book,
    update to database'''
    # get new title
    print("\nUpdating book title:")
    new_title = input("Enter the updated book title: ")
    # update info in database
    try:
        cursor.execute('''
                       UPDATE book SET title = ? WHERE id = ?''',
                       (new_title, update_b_id))
        edb.commit()
        print("Book title successfully updated!")
    except sqlite3.Error:
        print("Update unsuccessful. Try again")
        edb.rollback()


def update_author_id(cursor, edb, update_b_id):
    '''Ask user for new author for a specific book,
    validate against author list, update to database'''
    print("\nUpdating book author ID")
    new_author_id = get_author_id(cursor)
    try:
        cursor.execute('''
                       UPDATE book SET authorID = ? WHERE id = ?''',
                       (new_author_id, update_b_id))
        edb.commit()
        print("Book author id successfully updated!")
    except sqlite3.Error:
        print("Update unsuccessful. Try again")
        edb.rollback()


def update_author_info(cursor, edb, update_b_id):
    '''print book author details for specific book, ask
    user what to update, update author info to database'''
    print("\nUpdating author info")
    # print author info for book for user to review
    cursor.execute('''SELECT book.title, book.authorID,
                   author.name, author.country
                   FROM book
                   INNER JOIN author ON book.authorID = author.id
                   WHERE book.id = ?''',
                   (update_b_id, ))
    b_author_info = cursor.fetchone()
    b_author_id = b_author_info[1]
    print(f'''---------------------------------------------
Book Title: {b_author_info[0]}
Author's Name: {b_author_info[2]}
Author's Country: {b_author_info[3]}
---------------------------------------------''')
    # ask user if theyd like to update the author name, country or both
    while True:
        try:
            a_update_choice = int(input('''Would you like to:
1: Update the Author's name
2: Update the Author's country
3: Update both the Author's name and country
Choice selection: '''))
            if a_update_choice in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Try again!")
        except ValueError:
            print("Invalid input. Try again!")

    # update author name
    if a_update_choice == 1:
        new_a_name = input("Please enter the updated author name: ")
        try:
            cursor.execute(
                '''UPDATE author SET name = ? WHERE id = ?''',
                (new_a_name, b_author_id))
            edb.commit()
            print("Author name successfully updated!")
        except sqlite3.Error:
            print("Update unsuccessful. Try again")
            edb.rollback()
    # update author country
    elif a_update_choice == 2:
        new_a_country = input("Please enter the updated author country: ")
        try:
            cursor.execute(
                '''UPDATE author SET country = ? WHERE id = ?''',
                (new_a_country, b_author_id))
            edb.commit()
            print("Author country successfully updated!")
        except sqlite3.Error:
            print("Update unsuccessful. Try again")
            edb.rollback()
    # update both author name and country
    elif a_update_choice == 3:
        new_a_name = input("Please enter the updated author name: ")
        new_a_country = input("Please enter the updated author country: ")
        try:
            cursor.execute(
                '''UPDATE author SET name = ?, country = ? WHERE id = ?''',
                (new_a_name, new_a_country, b_author_id))
            edb.commit()
            print("Author name and country successfully updated!")
        except sqlite3.Error:
            print("Update unsuccessful. Try again")
            edb.rollback()


# Specific Functionalities
def add_new_book(cursor, edb):
    '''collects info from user about books, validates info,
    adds book to book table in database'''
    # collect book data from user
    print("\nTo add a new book to the database enter the following info:")
    # title
    b_title = input("Please enter the book's title: ")

    # qty
    while True:
        try:
            b_qty = int(input("Please enter how many books are in stock: "))
            if b_qty >= 0:
                break
            else:
                print("Quantity cannot be negative. Try again!")
        except ValueError:
            print("Invalid input! Try again!")

    # author
    b_author_id = get_or_add_author(cursor, edb)

    try:
        # id
        cursor.execute("SELECT MAX(id) FROM book")
        max_id = cursor.fetchone()[0]
        b_id = max_id + 1

        # add book to database
        cursor.execute(
            '''
            INSERT INTO book(id, title, authorID, qty)
                VALUES (?, ?, ?, ?)''', (b_id, b_title, b_author_id, b_qty)
        )
    # commit changes to database
        edb.commit()
        print("Book successfully added!")
    except sqlite3.Error:
        edb.rollback()
        print('Book addition unsuccessful!')


def update_book(cursor, edb):
    '''Default to update quantity, else user chooses other update
    options, respective function runs, update to database'''
    print("\nUpdating book")
    update_b_id = get_book_id(cursor)
    while True:
        update_choice_1 = input('''\nWould you like to update book quantity?
    1. Yes
    2. No, I'd like to update something else
    Please enter 1 or 2 based on your choice: ''')
        if update_choice_1 in ["1", "2"]:
            break
        else:
            print("Invalid input. Try again!")
    # execute choice 1
    if update_choice_1 == "1":
        update_qty(cursor, edb, update_b_id)
    elif update_choice_1 == "2":
        while True:
            update_choice_2 = input('''\nSelect what you would like to update:
    1. Book Title
    2. Book Author ID
    3. Book Author Information
    4. No updates required
    Please enter 1, 2, 3 or 4 based on your choice: ''')
            if update_choice_2 in ["1", "2", "3", "4"]:
                break
            else:
                print("Invalid input. Try again!")
        # execute choice 2
        if update_choice_2 == "1":
            update_title(cursor, edb, update_b_id)
        elif update_choice_2 == "2":
            update_author_id(cursor, edb, update_b_id)
        elif update_choice_2 == "3":
            update_author_info(cursor, edb, update_b_id)
        elif update_choice_2 == "4":
            print("No updates completed!")


def delete_book(cursor, edb):
    '''get book id, confirm, delete book from database'''
    print("\nDeleting book:")
    del_b_id = get_book_id(cursor)
    while True:
        del_confirm = input(f"Are you sure you want to "
                            f"delete book {del_b_id} (y/n)").lower()
        if del_confirm == 'y':
            try:
                cursor.execute('''DELETE from book WHERE id = ?''',
                               (del_b_id, ))
                edb.commit()
                print("Book deletion successful!")
                break
            except sqlite3.Error:
                edb.rollback()
                print('Book deletion unsuccessful!')
        elif del_confirm == 'n':
            break
        else:
            print("invalid input! Try again")


def search_books(cursor):
    '''get valid book id, print info for that book'''
    print("\nSearching for specific book:")
    select_b_id = get_book_id(cursor)
    # get book info and print details:
    cursor.execute('''SELECT book.id, book.title, author.name, book.qty
                   FROM book
                   INNER JOIN author ON book.authorID = author.id
                   WHERE book.id = ?''',
                   (select_b_id, ))
    book_data = cursor.fetchone()
    print(f'''---------------------------------------------
Book ID: {book_data[0]}
Title: {book_data[1]}
Author: {book_data[2]}
Quantity: {book_data[3]}
---------------------------------------------''')


def view_all_details(cursor):
    '''print book details using both author and book tables'''
    cursor.execute('''
                   SELECT book.title, author.name, author.country
                   FROM book
                   INNER JOIN author ON book.authorID = author.id  ''')
    all_details = cursor.fetchall()
    print("Details")
    for book in all_details:
        print(f'''---------------------------------------------
Book Title: {book[0]}
Author's Name: {book[1]}
Author's Country: {book[2]}
---------------------------------------------''')


# ---------Shelf Track Program------------
try:
    with get_db_connection() as edb:
        cursor = edb.cursor()
        create_btable(cursor, edb)
        create_atable(cursor, edb)
        while True:
            menu = input('''\nSelect one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit
Enter choice: ''')
            if menu == "1":
                add_new_book(cursor, edb)
            elif menu == "2":
                update_book(cursor, edb)
            elif menu == "3":
                delete_book(cursor, edb)
            elif menu == "4":
                search_books(cursor)
            elif menu == "5":
                view_all_details(cursor)
            elif menu == "0":
                print("\nExiting Program...\n")
                break
            else:
                print("Invalid input! Try again!")
except sqlite3.Error:
    print("Database Error found. Try again")
