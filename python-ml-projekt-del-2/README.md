1) Målet:

Målet med det här projektet vår att bygga en AI-lösning som kan beräkna sannölighet för 
att en kvinna har Diabetes Typ 2 eller inte;

För mer information om motivation, vänligen hänvisa till följande dokument:

Länk till Projekt Del 1
https://docs.google.com/document/d/1sG-J37nJmogzOaU9FcY4SksrW02IixNxd2IWHhA4MwM/edit?tab=t.0

2) Data:

 Det är et binärt klassificering problem, och för att bygga lösningen anvandes den märkta datan från
 “the National Institute of Diabetes and Digestive and Kidney Diseases”. Det innehåller olika 
 hälsosparametrar som potentiellt kan definiera resultatet. 

Imputation och skalning:
 - För att skapa lösningen implementerades dataanalys och Imputation;
 - Extrema värden var raderade;
 - För imputering av saknade värden implementerades kalkulation av Median;
 - Slutlig skalning gjordes med z-standardisering (StandardScaler) eftersom variablerna är kontinuerliga;


För initial dataanalys och bearbetning, vänligen hänvisa till följande dokument:

https://github.com/AniaAlex/Pythonprogrammering-for-AI-utveckling-AnnaAlexeeva/blob/main/python-ml-projekt-del-1/diabetes_kvinnor.ipynb

4) Modellen:

Det är ett klassificeringsproblem och deep neural networks i Keras 
Sequential() med cross entropy (loss=‘binary_crossentropy’) kan används.
Binary crossentropy används som förlustfunktion, 
vilket är lämpligt för binära klassificeringsproblem.

4) Den tränade modellen visar relativt stabila resultat.

-  Den bästa "accuracy" är cirka 90%;
- "Accuracy" och "Validation accuracy" visar resultat som ligger nära varandra;
- "loss" och "validation loss" visar en stadig minskning;


Som en slutsats, Den nuvarande modellen kan kalkylera sannolikheten för att 
en kvinna har diabetes med mer än 80% noggrannhet.

Binär klassificeringsproblem: I det här fallet förutspår modellen ett av två möjliga utfall. 

Det är viktigt att komma ihåg att data storlek och kvalitet kan påverka resultaten.

5) Punkter kring AI-lösning och etik inom medicine:

- Lösningen tränades på öpen informationskälla;
- Lösningen skapades för studieändamål och kan inte användas för verkliga beslut;












 

 