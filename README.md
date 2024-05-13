# CaseOpgave1

Projectet består af flere forskellige dele: "Databaser", selve systemet og hjælpe klasser dertil:

## Databaserne
ReadFiles.py indlæser filen Modern_Library_Top_100_Best_Novels.xlsx til en pandas DataFrame og gemmer
de relevante kolonner til filen libraryBooks.xlsx.
generateUsers.py bruger python modulet faker til at generere navne og adresser til virtuelle brugere og
gemmer dem i filen user_data.xlsx.

## Systemet
Library.py tilgår den pandas DataFrame der initieres af Readfiles.py og indeholder funktioner til at
manipulere denne, f.eks registrere om en bog er lånt eller reserveret. Library class'en er et singleton
objekt for at sikre at alt registreres i samme dataframe.
User.py definerer en class for et user objekt som bruges af UserManagement.py, med funktioner til at 
registrere en brugers handlinger, f.eks udlån og aflevering af bøger.
UserManagement definerer en singleton class som tilgår og manipulerer user_data.xlsx filen, samt anvender user objekter defineret i User.py til dette.

## UI

UIMenu.py er vores tekstbaserede bruger flade. Den bruger de førnævnte moduler til at logge en bruger ind 
og tilgå bibliotekets bogdatabase til søgninger, lån og reservation.

## Hjælpe klasser
