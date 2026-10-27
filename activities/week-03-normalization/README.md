# Week 3: normalization in a workbook

Two spreadsheets for Wednesday of week 3. Nothing here is marked. Each one opens in Excel, Google Sheets or LibreOffice: the cells are plain, with no formulas or macros.

## `college-normalization.xlsx`: together, in the morning

One sheet of college records as the registrar keeps it: one row per student, per course, per term. We take it to third normal form together, one sheet per form. The `0NF` sheet is filled in; `1NF`, `2NF` and `3NF` are empty and we fill them in class. Every sheet starts from the one before it. The `README` sheet inside the workbook says what goes in which cell.

Open it before the session starts. If the file does not open on your laptop, upload it to Google Sheets.

## `clinic-normalization.xlsx`: in groups, in the afternoon

A vet clinic keeps one spreadsheet, one row per visit. In your group, take it to third normal form the same way: `1NF`, then `2NF`, then `3NF`, each sheet starting from the one before it.

Rules, also on the workbook's `README` sheet:

- One workbook per group. Work on the sheets in order and do not skip a form.
- B1 on each form sheet: the reason for that form in one sentence. B3: the key after that form, the columns that pick out exactly one row. B4: any fork you hit (two valid ways to split the data) and the choice your group made, with one reason.
- A table is a bold name, a header row, then the rows. One blank row between tables. Name a linking table after the two tables it links, for example `pet_owners`.
- On the `3NF` sheet, end with a table called `relationships`: parent, child, one-to-many or many-to-many, and where the foreign key is.

The data is ambiguous on purpose. Two groups can reach different valid designs. What matters is that every step has a reason and every fact is stored once.

**Presenting:** 4 to 5 minutes per group. Walk the sheets in order and show the process, not only the final tables. Name one fork and say why you chose your side.

**Hand-in:** every member commits the group's workbook to `week-03/hackathon/normalization/clinic-normalization.xlsx` in their own `2494-Gen-AI-CN/<FirstnameLastname>` repository, on `main`, and pushes.

## Words used in both workbooks

- **Key:** the column or columns that pick out exactly one row. A **composite key** is a key made of more than one column.
- **1NF:** one value per cell, no lists. A comma list becomes one row per item.
- **2NF:** every column depends on the whole key, not on part of it.
- **3NF:** no column depends on another column that is not the key.
- **Linking table:** a table whose key is two foreign keys, used when a row on each side can relate to many rows on the other.
