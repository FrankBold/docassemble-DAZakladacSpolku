# Poznámky v vývoji.

## Zakladatelské dokumenty

- U kroku tři už víme, jak chtějí uživatelé spolek zakládat, tedy to tomu rozvnou přizpůsobíme. Na začátku bude kontrola, kdyby se náhodou vrátili zpět a změnili to, ať se v kroku tři načte správná věc.
- Pokud zakládáme ustavující schůzí, přidáme krok navíc po vygenerování stanov. Jinak se vytváří všechny dokumenty najednou.

---
attachment:
  name: Stanovy spolku
  filename: Stanovy_spolku
  variable name: stanovy
  docx template file: Stanovy.docx
  update references: True
  valid formats:
    - docx
---
attachment:
  name: Souhlas s umístěním sídla spoklku
  filename: Souhlas
  variable name: souhlas
  docx template file: SouhlasSidlo.docx
  valid formats:
    - docx