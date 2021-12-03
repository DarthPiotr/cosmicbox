# COSMICBOX
Automation basics project

## Regulator temperatury pomieszczenia


##### Opis projektu:
Pomieszczenie jest idealnym prostopadłościanem bez mebli w środku. Na jednej ze ścian znajduje się 
okno, które możemy otwierać wedle uznania. Dla uproszczenia obliczeń przyjmujemy, że 
temperatura jest taka sama w całej objętości pomieszczenia.

Straty ciepła zależą od powierzchni i materiału ścian oraz wielkości i stopnia otwarcia okna. Źródło 
ciepła (grzejnik elektryczny) ogrzewa pomieszczenie równomiernie w całej objętości i jest sterowane
przez regulator PID.

Wszystkie ściany wykonane są z tego samego materiału. Przyjmujemy założenie, że temperatura na 
zewnątrz jest niższa niż temperatura docelowa.

##### Schemat:
![Schemat:](https://github.com/DarthPiotr/cosmicbox/blob/main/obrazy/schemat.png)

##### Obliczenia:

###### Ciepło dostarczone:

<table><tr><td> Q<sub>d</sub>(n) = η*P*u(n) </td></tr></table>

###### Straty ciepła:

<table><tr><td> Q<sub>S</sub>(n) = (U<sub>1</sub>S<sub>1</sub> + xU<sub>2</sub>S<sub>2</sub>)(T(n) - T<sub>Z</sub>) </td></tr></table>

###### Objętość pomieszczenia:

<table><tr><td> V = A*B*C </td></tr></table>

###### Równanie różnicowe:

<table><tr><td> T(0) = T<sub>0</sub> </td></tr></table>
<table><tr><td> T(n+1) = ((Q<sub>d</sub>(n) - Q<sub>S</sub>(n))*T<sub>p</sub>) / (c*d*V) + T(n) </td></tr></table>



##### Legenda do obliczeń:

η - poprawność  urządzenia  
P - maksymalna moc urządzenia  
u(n) - sygnał z regulatora  
Q(n) - Ciepło dostarczone do pomieszczenia  
U<sub>1</sub> - współczynnik przenikania ciepła przez ściany  
U<sub>2</sub> - współczynnik przenikania ciepła przez okno  
S<sub>1</sub> - powierzchnia ściany (wymiany ciepła)  
S<sub>2</sub> - powierzchnia okna (wymiany ciepła)  
x - współczynnik  otwarcia okna  
T(n) - poprzednia temperaura  
T<sub>Z</sub> - temperatura na zawnąrz  
T<sub>0</sub> - temperatura początkowa pomieszczenia  
c - ciepło właściwe powietrza  
d - gęstość powietrza  
