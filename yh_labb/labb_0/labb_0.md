> - om studenter, förnamn, efternamn, personnummer, email
> - utbildare kan vara konsulter
> - de planerar att anställa fasta utbildare (BONUS)
> - utbildningsledare och deras personuppgifter
> - utbildningsledare har hand om 3 klasser
> - kurser med namn, kurskod, antal poäng, kort beskrivning av kursen
> - program har ett antal kurser knutna till sig
> - ett program blir beviljat i tre omgängar, dvs att det finns 3 klasser
> - det finns även fristäende kurser (BONUS)
> - konsulter, deras företag, företagsinfo som organisationsnummer, har F-skatt, address, hur mycket de tar i arvode per timma
> - YrkesCo har tvà anläggningar, en i göteborg och en i stockholm, i framtiden kanske de kommer expandera till flera orter (BONUS)

> känsliga personuppgifter bör läggas i egna entiteter, eftersom det blir lättare att kontrollera vem som far access till dem tabellerna.  

> är det nagra extra krav ni känner behövs, men YrkesCo missat att skriva ned, kan ni lägga till det, men behöver framgả vilka krav ni vill lägga till. Likas om det är ngot krav som ni känner kan förtydligas, sà kan ni ocksà skriva till det.

## Uppgift 0 - datamodellering

### 0_b

b) Gör en konceptuell modell baserat pa kravspecifikationen.

### 0_c

c) Skriv relationship statements för varje entitet.

### 0_d

d) Bygg nu en logisk modell baserat pá den konceptuella

### 0_e

e) Skapa fysisk modell baserat pà den logiska modellen

### 0_f

f) Argumentera för att modellen du skapar uppnar 3NF.

## Uppgift 1 - implementation

> Implementera din fysiska modell i postgres. Alla SQL script ska finnas i din labbfolder. För implementation ska du

### 1_a

a) skapa tabellerna

### 1_b

b) fylla i med fakedata (räcker med ett par records i varje tabell)

### 1_c

c) Gör ett/flera skript med SQL queries där du testar att joina olika tabeller för att plocka ut information. Ex kan du ta reda pa en specifik klass vilken utbildningsledare den har, vilka kurser den har, hur manga kurser, vilka utbildare som undervisar vilka kurser där.