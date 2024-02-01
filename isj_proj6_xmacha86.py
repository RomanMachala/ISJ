
class Polynomial:

    def __init__(self, *coefficient, **kwargs):
        
        self.arguments=[]       #Zde bude ulozen nas vysledny polynom
        for i in coefficient:       #Projde vsechny koeficienty, ktere jsme dostali jako argument
            if isinstance(i, list):     #Pokud se jedna o list, muzeme se na nej primo odkazat
                self.arguments=i 
        if not self.arguments:      #Pokud nebyl prirazen list, bude selfargument prazdny a muze se jednat bud o samostatna cisla nebo kwargs (ve tvaru x=..)
            if coefficient:
                self.arguments=list(coefficient) #Pokud se jedna o cisla, udelame z nich list a odkazeme se na nej
            else:
                for name,value in kwargs.items():   #Pokud se jedna o parametry ve tvaru (x=... atd)
                    for i in range(1 + int(name.split("x")[1])-len(self.arguments)):    #Jeden po druhem rozdelime dle 'x'
                        self.arguments.append(0)                                        #Naplnime list 0, dokud nedojdeme na index, kde ma dany koeficient byt
                    self.arguments[int(name.split("x")[1])]=value                       #A na tento index tento koeficient dame
                    #Je to z duvodu, ze parametry mohou byt zadavany v libovolnem poradi
        for i in range(len(self.arguments)-1, 0, -1): #Smazeme prebytecny pocet nul
            if self.arguments[i]==0:
                del self.arguments[i]
            else:
                break #Pokud narazime na nenulovou hodnotu ukoncujeme cyklus
    def __str__(self):
        result = ""     #String, do ktereho budeme ukladat vysledny polynom 
        for i, coef in enumerate(self.arguments):        #i = mocnina, koeficinet je "coef"x^i
            if coef != 0:                            #Pokud neni koeficient nulovy provede se nasledujici, pokud je, pokracuje se dale (nulove koeficienty nezahrnujeme)
                if i == 0:  #Toto je absolutni clen neboli x^i = x^0, zkontroluje se pouze znamenko a potom se vypise jeho abs hodnota
                    result = f"{'+' if coef > 0 else '-'} {abs(coef)} {result}"
                elif i == 1:    #Pokud se mocnina rovna 1
                    if coef in (1, -1):    #Pokud koeficient je roven 1 / -1, zkontroluje se znamenko, vypise se pouze x
                        result = f"{'+' if coef > 0 else '-'} x {result}"
                    else:   #Pokud koeficient je jine cislo nez jedna vypise se "cislo"x (samozrejme se predtim zase kontroluje znamenko koeficientu)
                        result = f"{'+' if coef > 0 else '-'} {abs(coef)}x {result}"
                else: #Pokud umocnujeme na neco jineho nez je 1
                    if coef in (1, -1):
                        result = f"{'+' if coef > 0 else '-'} x^{i} {result}"    #Zkontroluje se znamenko a vypise se prislusna mocnina
                    else:
                        result = f"{'+' if coef > 0 else '-'} {abs(coef)}x^{i} {result}"  #Zkontrolujeme znamenko a vypiseme prislusnou mocninu s danym koeficientem

        if not result:  #Pokud neni ve stringu nic ulozeno, vracime hodnotu 0
            result = "0"
        if result[0] == "+":        #Vznikal problem, ze polynom zacinal + nebo - (o to se staraji tyto podminky)
            result = result.lstrip('+') #Odstrani ze zacatku +
        if result[0] == "-":
            result = result.lstrip('-') #Odstrani ze zacatku -
        
        if result[0] != "0":
            result = result.lstrip(' ') #Odstrani prebytecnou mezeru ze zacatku
            result = result[:-1]    #Na konci stringu jeste byla mezera navic, ktera taky je potreba odstranit

        return result   #Vraceni vysledneho stringu
    
    def __eq__ (self, other):       #Porovnavani Polynomu
        if len(self.arguments) != len(other.arguments): #Porovname delku polynomu, pokud se lisi v delce, nemohou byt stejne
            return False
        for a, b in zip(self.arguments, other.arguments):   #Funkce zip vezme jednotlive cleny obou polynomu a porovna je mezi sebou
            if a != b:                                      #Pokud se lisi alespon jeden clen vracime hodnotu false
                return False
        return True                                         #V opacnem pripade se polynomy jednaji a vracime true

    def __add__(self, other):   #Scitani Polynomu
        temp_bigger=self.arguments  #docasy vetsi list
        temp_lower=other.arguments  #docasny mensi list
        if len(other.arguments) > len(self.arguments):  #Zjistime, ktery z poskytnutych listu je vetsi
            temp_bigger = other.arguments               #a dame jej do temp_bigger
            temp_lower = self.arguments

        for i in range(len(temp_lower), len(temp_bigger)):        #Doplnime mensi pocet prvku nulami
            temp_lower.append(0)
        return_list=self.arguments[:]      #Finalni list, ktery bude navratovou hodnotou (bez reference)
        #V tento moment maji oba temp listy (lower, bigger) stejnou veliksot (jeden je doplnen nulami)
        i = 0               #Index ve finalnim listu
        for first, second in zip(temp_lower, temp_bigger):          #Pomoci funkce zip secteme vsechny prvky obou polynomu
            return_list[i]=first + second       #Do finalniho listu secteme hodnoty z obou listu
            i += 1          #Zvysime promennou
        return Polynomial(return_list)                  #Vratime Polynom souctu obou listu

    def __pow__(self, n): #Umocneni polynomu 
        if n == 1:
            return self
        if n > 1:   #Muzeme umocnovat pouze kladnym cislem
            m = len(self.arguments)     #Ziskame velikosti obou polynomu (nasobime jeden sam se sebou - oba jsou stejne) 
            n = len(self.arguments)
            tmp = [0]*(m+n+1)           #Vytvorime si pole o dostatecne velikosti inicializovane na same nuly
            for x in range(1, n):       #Venkovni cyklus, urcuje kolikrat budeme nasobit mezi sebou
                for i in range(0, m):   
                    for j in range(0, n):   #Vnitrni cykly, pomoci nich vynasobime vzdy 
                        if x == 1:          #pri prvni iteraci vynasobime dva puvodni polynomy mezi sebou
                            tmp[i+j] += self.arguments[i]*self.arguments[j]
                        else:
                            tmp[i+j] += tmp[i]*self.arguments[j]    #Pri dalsich iteracich ale musime nasobit jiz drive vynasobeny polynom
            return Polynomial(tmp)      #Vracime polynom
            
    def at_value(self, x1, x2 = "NaN"):
        #Vypocet hodnoty daneho polynomu
        result=0    #Implicitne nastavime hodnotu na 0
        for index, value in enumerate(self.arguments):  #Z argumentu si vytahneme dane cislo a index, na kterem jsme v listu
            #cislo x umocnime na dany index a vynasobime cislem nachazejicim se na danem indexu
            result += (x1 ** index) * value               #Ulozime do nasi promenne pro vysledek
           #Nastavime vysledek na hodnotu prvniho polynomu
        if x2 != "NaN": #Pokud je zadana druha hodnota, vracime rozdil techto polynomu (druheho a prvniho)
            for index, value in enumerate(self.arguments):
                #Stejna myslenka jako u prvniho pocitani hodnoty
                result_x2 = 0
                result_x2 += (x2 ** index) * value
                result = result_x2 - result
                #Jediny rozdil je, ze pokud pocitame hodnotu pro druhe cislo, odecteme od tohoto polynomu puvodni hodnotu
        return result   #Vracime vysledek pocitani
    
    def derivative(self):   #derivace polynomu
        derivation = self.arguments #Inicializujeme si list pro vysledek nasi derivace
        del derivation[0]       #Odstranime konstantu (derivace konstanty je 0)
        for index, value in enumerate(derivation):  #Projdeme vsechny prvky, ktere nam zustaly
            derivation[index] = value * (index + 1) #Vynasobime cislo na danem indexu indexem o pozici dale (protoze jsme je posunuli odstranenim konstanty)
        return Polynomial(derivation)   #Vratime vyslednou derivaci

       




def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == "__main__" : 
    test()