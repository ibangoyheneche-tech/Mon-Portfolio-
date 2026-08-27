# Avant-propos
**Crackme :** Guessy (Hackopole)  
**Difficulté :** Intro <br>
Dans ce write-up, nous allons résoudre ce crackme grâce à une analyse statique via Ghidra et un peu de Python. <br>

# Analyse préliminaire
On regarde d'abord le type du fichier.
```bash
$ file guessy
guessy: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```
Le fichier est un exécutable ELF 64 bits. <br>
La commande strings ne donne rien. <br>
On va exécuter guessy une première fois pour voir ce que ça donne.
```bash
$ ./guessy
Give me the flag:
test
Well it does not begin well for you.
```
Bien sûr ça donne rien, on va passer sur Ghidra.

# Analyse statique
On suit le flot d'exécution.

## 1. Main
```c
undefined8 main(void)

{
  char local_28 [32];
  puts("Give me the flag:");
  fgets(local_28,0x20,stdin);
  validate(local_28);
  return 0;
}
```
La fonction main demande une entrée utilisateur et s'en sert comme argument pour la fonction `validate`.

## 2. Validate
```c
  if ((((*param_1 == 'F') && (param_1[1] == 'C')) && (param_1[2] == 'S')) && (param_1[3] == 'C')) {
    if (param_1[4] == '{') {
      puts("Ok so I see we have an understanding. Let\'s begin the difficult part now.");
      difficult_part();
```
Les quatre premiers caractères saisis sont comparés à FCSC{ ce qui est logique c'est le début de la syntaxe du flag.
On a nos quatre premiers caractères. Ensuite une autre fonction est appelée `difficult_part`.

## 3. Difficult_part
Dans cette fonction on nous demande d'abord un input. Il y a une vérification de cette entrée et si on trouve, on passe au bout du flag suivant. <br>
On change d'abord le type de local_18 (qui contiendra les entrées utilisateur tout au long du programme) par char[16] car on a :
```c
fgets(local_18,0x10,stdin);
```

On obtient donc :
```c
    if (((((local_18[0] == 'e') && (local_18[1] == '7')) && (local_18[2] == '5')) &&
        ((local_18[3] == '5' && (local_18[4] == '2')))) &&
       ((local_18[5] == 'c' && ((local_18[6] == 'f' && (local_18[7] == '6')))))) {
```
La suite du flag est donc e7552cf6. <br>
```c
        if ((((((int)local_18[0] & 0x7fffffffU) == 0x34) && (((int)local_18[1] & 0x7fffffffU) == 99)
             ) && (((int)local_18[2] & 0x7fffffffU) == 0x65)) &&
           (((((int)local_18[3] & 0x7fffffffU) == 0x32 && (((int)local_18[4] & 0x7fffffffU) == 0x65)
             ) && ((((int)local_18[5] & 0x7fffffffU) == 0x35 &&
                   ((((int)local_18[6] & 0x7fffffffU) == 0x61 &&
                    (((int)local_18[7] & 0x7fffffffU) == 100)))))))) {
```
La conversion hexadécimale de 100 est 0x64. On peut le vérifier avec la fonction `hex` en Python.
```python
print(hex(100))
```
En python on va prendre notre série valeurs hexadécimales puis on va l'afficher en caractère lisible.
```python
hex1 = "0x34 0x63 0x65 0x32 0x65 0x35 0x61 0x64"
res1 = ""
for h in hex1.split():
    nombre = int(h, 16)
    caractere = chr(nombre)
    res1 += caractere
print(res1)
```
Le résultat est 4ce2e5ad. <br>
Le masque 0x7fffffff est ici inutile car il met le bit de signe à 0. Or les caractères ASCII sont tous positifs.
```c
            if ((((((int)local_18[0] & 0x1fffffffU) == 0x30) &&
                 (((int)local_18[1] & 0x1fffffffU) == 0x62)) &&
                (((int)local_18[2] & 0x1fffffffU) == 0x62)) &&
               (((((int)local_18[3] & 0x1fffffffU) == 0x30 &&
                 (((int)local_18[4] & 0x1fffffffU) == 0x39)) &&
                ((((int)local_18[5] & 0x1fffffffU) == 0x35 &&
                 ((((int)local_18[6] & 0x1fffffffU) == 0x34 &&
                  (((int)local_18[7] & 0x1fffffffU) == 0x66)))))))) {
```
Ici même logique.
```python
hex2 ="0x30 0x62 0x62 0x30 0x39 0x35 0x34 0x66"
res2 = ""
for h in hex2.split():
    nombre = int(h,16)
    caractere = chr(nombre)
    res2 += caractere
print(res2)
```
On trouve 0bb0954f. <br>
Le masque 0x1fffffff est aussi inutile. Il permet de mettre à 0 les trois bits de poids forts.
Les caractères ASCII sont compris entre 0x00 et 0x7f. 
Notre caractère pour effectuer le & va être converti en int donc en 32 bits.
On va simplement lui rajouter des 0. Donc les trois bits de poids fort sont déjà égaux à 0.
Le masque 0x1FFFFFFF ne modifie donc jamais la valeur.
```c
                if ((((((byte)(local_28 ^ local_18[0]) == 1) &&
                      ((byte)(local_27 ^ local_18[1]) == 0x54)) &&
                     ((byte)(local_26 ^ local_18[2]) == 0x55)) &&
                    (((byte)(local_25 ^ local_18[3]) == 0x51 &&
                     ((byte)(local_24 ^ local_18[4]) == 9)))) &&
                   (((byte)(local_23 ^ local_18[5]) == 7 &&
                    (((byte)(local_22 ^ local_18[6]) == 0x57 && (local_18[7] == local_21)))))) {
```
On a donc un XOR à résoudre entre les caractères saisis à l'étape précédente (local_18) et saisis maintenant (local_28,local_27, etc.).
Le dernier caractère quant à lui, est égal au dernier caractère saisi précédemment donc f.
```python
hex3 = "0x1 0x54 0x55 0x51 0x9 0x7 0x57"
res3 = ""
for h, i in zip(hex3.split(), hex2.split()):
        nombre = int(h,16) ^ int(i,16)
        caractere = chr(nombre)
        res3 += caractere

# dernier caractére
res3 += "f"
print(res3)
```
On obtient 167a02cf. <br>
Ensuite on a un dernier appel de fonction avec `most_difficult_part`.

## 4. Most_difficult_part
```c
    if (local_18[0] == '}') {
      puts("Congratulations, you\'ve guessed the flag !");
```
Le dernier caractère est juste }. <br>
Nous avons donc reconstruit le flag : FCSC{e7552cf64ce2e5ad0bb0954f167a02cf}.
