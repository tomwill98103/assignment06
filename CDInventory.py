#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# TWilliams, 2020-Aug-16, Created File
# TWilliams, 2020-Aug-16, Wrote/Updated Data Processor functions
# TWilliams, 2020-Aug-23, Wrote/Updated FileProcessor, and IO functions
# TWilliams, 2020-Aug-24, Debug, docstrings, documentation
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
tupNewCD = () # holds new CD info
strLoadMsg = 'loading data...\n' # load confirmation message


# -- PROCESSING -- #
class DataProcessor:
    """Add and deleting data to list in memory"""
    
    @staticmethod
    def add_cd(new_CD, table):
        """Adds new CD to list in memory
        
        Takes user input as tuple and produces entry as dictionary
        Adds dictionary to list and returns revised inventory
        
        Args:
            new_CD (tuple):string entries for new CD
            table (list of dict): 2D data structure that holds data
            
        Return:
            table (list of dict): 2D data structure that holds data 
            """
        dicRow = {'ID': int(new_CD[0]), 'Title': new_CD[1], 'Artist': new_CD[2]}
        table.append(dicRow)
        return table

    @staticmethod
    def del_cd(del_id,table):
        """Deletes CD from list in memory
        
        Takes user input as int and searches list for corresponding row
        Returns revised table
                
        Args:
            del_id (int): entries for new CD
            table (list of dict): 2D data structure that holds data
            
        Return:
            table (list of dict): 2D data structure that holds data 
            """
        intRowNr = -1
        for row in table:
            intRowNr += 1
            if row['ID'] == del_id:
                del table[intRowNr]
                break
        return table
        

class FileProcessor:
    """Processing the data to and from text file"""
    
    @staticmethod
    def check_file(file_name):
        """Function to check for existence of file and create if needed

        Imports OS module to check for file
        Creates empty if doesn't exist

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            None.
        """
        # check to see if file exists, if not create
        import os
        while not os.path.exists(file_name):
            objFile = open(file_name, 'a')
            objFile.close()


    @staticmethod
    def read_file(file_name, message, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table.

        Args:
            file_name (string): name of file used to read the data from
            message (string): confirmation message
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
            
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()
        print(message)

    @staticmethod
    def write_file(file_name, table):
        """Function to write inventory to file

        Reads data row by row from 2D table
        writes each row as strings to file.

        Args:
            file_name (string): name of file used to read the data from
            message (string): confirmation message
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice
                
    @staticmethod
    def msg_load(filename,table):
        """Loads data from file into memory
        
        Presents warning and gets user confirmtion
        If confirmed calls load function

        Args:
            None.

        Returns:
            None.

        """
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        str_yn = input('Type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if str_yn.lower() == 'yes':
            load_msg='reloading...\n'
            FileProcessor.read_file(filename, load_msg, table) # Call load function
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def add_cd(table):
        """Gets user input to add new CD to list in memory
        
        Takes user input as integer and strings and returns tuple. 
        Checks for duplicate and invalid ids
        
        Args:
            table (list of dict): 2D data structure that holds data
            
        Return:
            cd_id: integer id of cd
            cd_title: string title of cd
            cd_atrist: string artist of cd
            """
        while True:
            try:
                cd_id = int(input("Enter an ID: "))
                for cd in table:
                    if cd_id == cd['ID']:
                         print("Duplicate ID\nPlease try again")
                         break
                else:
                     break
            except ValueError:
                print("Invalid ID\nPlease enter an integer ID")
        
        cd_title = input('What is the CD\'s title? ').strip()
        cd_artist = input('What is the Artist\'s name? ').strip()
        return cd_id,cd_title,cd_artist
    
    @staticmethod
    def del_cd(table):
        """Function to get user input to delete CD from list in memory
        
        Takes user input as integer. 
        If found calls delete function
        If not found gives choice to restart or return to menu with original table
        Error handling for non-integer entries
        
        Args:
            table (list of dict): current inventory as 2D table
            
        Return:
            table (list of dict): current or revised inventory as 2D table
            """
        check_id = 1    
        while check_id == 1:
            try:
                del_id=int(input('Which ID would you like to delete? '))
                for cd in table:
                    if del_id == cd['ID']:
                        del_id=cd['ID']
                        check_id = 0
                        table=DataProcessor().del_cd(del_id,table) # Call delete function
                        print('The CD was removed\n')
                        break
                if check_id:
                    print('Sorry that ID does not exist.')
                    del_esc = input('\nType "m" to return to menu or any key to try again: ')
                    if del_esc == 'm':
                        IO.print_menu() # Call menu dispaly function
                        break
            except ValueError:
                print("Invalid ID\nPlease enter an integer ID")
        return table

    @staticmethod
    def msg_sav(filename,table):
        """Gets user input to save list in memory to file
        
        Takes user input as string. 
        Calls save function if user confirms
        
        Args:
            filename (string): name of save file
            table (list of dict): currently inventory in memory as 2D data structure that holds data
            
        Return:
            None
            """
        str_yn = input('Save this inventory to file? [y/n] ').strip().lower()
        if str_yn == 'y':
             FileProcessor().write_file(filename, table) # Call save function
             print('Inventory saved\n')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.\n')



# 1. When program starts, read in the currently saved Inventory
# 2.1 Check to see if file exists, if not create
FileProcessor.check_file(strFileName)
# 2.2 Load file and confirm to user
FileProcessor.read_file(strFileName,strLoadMsg,lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        # 3.2.1 display warning and get confirmation to call load function
        IO.msg_load(strFileName, lstTbl)
        # 3.2.2 shows inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        tupNewCD=IO.add_cd(lstTbl)
        # 3.3.2 Add item to the table
        lstTbl=DataProcessor.add_cd(tupNewCD,lstTbl)
        # 3.3.3 display updated inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.2 ask user which ID to remove and call del function if confirmed
        lstTbl = IO.del_cd(lstTbl)
        # 3.5.3 display updated inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory 
        IO.show_inventory(lstTbl)
        # 3.6.2 Ask user for confirmation and call save function
        IO.msg_sav(strFileName, lstTbl)

        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




