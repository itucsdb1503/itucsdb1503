Parts Implemented by Mehmet Emir Memmi
======================================
User interace that is provided is quite simple and easy to use. Basic functios that is provided are add, update, search and delete operations. Also
user can drop and initialize table with one click at their own expense. All tables have the same structure so the functions and their working instructions are generally the same.

 .. figure:: images/circuits.png
      :scale: 50 %
      :alt: can not load image

      Example of Circuits page.

Add Instructions
,,,,,,,,,,,,,,,,
* User should fill the related fields by the following instruction model
- **Name:** Text Entry
- **Length:** Number Entry
- **Width:** Number Entry
- **Left Corners:** Number Entry
- **Right Corners:** Number Entry
- **Longest Straight:** Number Entry
- **Country:** Text Entry
- **Constructed Year:** Number Entry

After the entries are filled press the 'Add Circuit' button for changes

Delete Instructions
,,,,,,,,,,,,,,,,,,,
- **ID:** Id number of the Intended Circuit
Press Delete Circuit for deleting.

Search Instructions
,,,,,,,,,,,,,,,,,,,
* User can enter any word that is aimed to be searched in any place of the name column of the circuit.
After that pressing the 'Search Circuit' button will refresh the page and bring the result of the search to the screen. User can leave it empty for listing all entries.
- **Name to Search:** Text Entry

Update Instructions
,,,,,,,,,,,,,,,,,,,
* User should fill the related fields by the following instruction model:
- **Id:** Number of the id of the intended row
- **Name:** Text Entry
- **Length:** Number Entry
- **Width:** Number Entry
- **Left Corners:** Number Entry
- **Right Corners:** Number Entry
- **Longest Straight:** Number Entry
- **Country:** Text Entry
- **Constructed Year:** Number Entry

After the entries are filled press the 'Update Circuit' button for changes


Instruction Notes For Other Tables
----------------------------------
Races:
,,,,,,
* **Entry Model:**
- **ID:** Id of the Race as Number Entry -Used in update and search operations
- **Name:** Text Entry
- **Fastest Lap Time:** Number Entry
- **Winner's Average Lap Time:** Number Entry
- **Average Lap Time:** Number Entry
- **First Position:** Text Entry
- **Track Circuit ID:** Number Entry - User should enter already existing Circuit id
- **Number of Laps:** Number Entry
- **Total Accidents:** Number Entry

Accidents:
,,,,,,,,,,
* **Entry Model:**
- **ID:** Id of the Accident as Number Entry -Used in update and search operations
- **Rider's Name:** Text Entry
- **Rider's Surname:** Text Entry
- **Race ID:** Number Entry - User should enter already existing Race Id
- **Is It Fatal:** Text Entry - Advised entry examples: Yes, No

