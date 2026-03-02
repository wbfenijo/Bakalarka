# Web stránka bakalárskej práce


---

## Informácie o študentovi

- **Meno študenta:** Adam Blažek
- **Názov práce:** Transformácia artefaktov vo vývoji softvéru.
- **Meno školiteľa:** Lukáš Radoský 
- **Kontakt na študenta:** blazek29@uniba.sk

---

## Zadanie práce

- **Anotácia:**  
V rámci vývoja softvéru poznáme niekoľko fáz, vrátane špecifikácie, návrhu, a implementácie. V rámci každej fázy vznikajú rôzne artefakty, napríklad diagramy tried v rámci návrhu alebo zdrojový kód v rámci implementácie. Automatizovaná transformácia artefaktov z jednej fázy vývoja na artefakty ďalsích fáz vývoja by umožnila rýchlejší vývoj softvéru, a je preto predmetom výskumu. Analyzujte existujúce prístupy pre transformáciu zvoleného typu artefaktu v softvérovom vývoji, napríklad transformáciu prípadov použitia na sekvenčný diagram. Navrhnite a implementujte prístup pre zvolený problém, pričom môžete aj nadviazať na existujúce práce. Svoju implementáciu vyhodnoťte na vzorke dát.

- **Cieľ práce:**  
implementácia prístupu pre transformáciu artefaktov vývoja softvéru

---

## Zdroje a odkazy

- **Články:**  
  - [Automatic generation of sequence diagrams and updating domain model from use cases.](https://www.thinkmind.org/articles/softeng_2015_4_30_55074.pdf)
  - [Generating Sequence Diagram from Natural Language Requirements](https://ieeexplore.ieee.org/document/9582297)
  - [Automated Derivation of UML Sequence Diagrams from User Stories: Unleashing the Power of Generative AI vs. a Rule-Based Approach](https://dl.acm.org/doi/abs/10.1145/3640310.3674081)
  - [A semi-automatic approach to translating use cases to sequence diagrams](https://ieeexplore.ieee.org/abstract/document/779011)
  - 
- **Východiskové záverečné práce:**  
  - [Datasety v softvérovom inžinierstve](https://opac.crzp.sk/?fn=detailBiblioFormChildI2FCAF&sid=71F69C32541FA50939647AB0024D&seo=CRZP-detail-kniha)
  - [Generovanie UML modelu z prípadov použitia](https://opac.crzp.sk/?fn=detailBiblioForm&sid=9A7D98113A4E7D6F04A971A0EB46)  

---

[Priebežná verzia bakalárskej práce](https://www.overleaf.com/read/wkdmrwcgzvjm#60a968)

---

## Týždenný denník aktualizácií

| Dátum | Popis  |
|-------|------------------|
| 06.10.-12.10. | Úvodný náhľad do problematiky, prvé články a práce |
| 20.10.-26.10. | Prvý kód, jednoduchý zero shot, spracovanie článkov do práce| 
| 03.11.-09.11. | Skúška zero shot s use case-om, vytvorenie klasy pre OpenAI, nájdenie datasetu a AI modelov| 
| 17.11.-23.11. | Spracovanie datasetu, prvý script pre judge-a, jednoduché prompty do viacerých modelov| 
| 01.12.-07.12. | Pokračovanie v skripte pre judge-a, prvé výsledky, spracovanie do .csv súborov | 
| 08.12.-14.12. | Návrh skriptu pre koreláciu v dátach, zlyhanie pre chybné dáta | 
| 16.02.-22.02. | Skript pre opravu dát, pridané nové modely, veľká refaktorizácia, stratified split datasetu pre trénovanie LLM| 




