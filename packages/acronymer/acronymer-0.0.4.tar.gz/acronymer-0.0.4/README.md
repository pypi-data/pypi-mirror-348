# Acronym Tools

A collection of functions to generate creative acronym interpretations based on a given context.

## Usage

### Generate Acronym Interpretations

Generates full-form interpretations for one or more acronyms based on provided context and number of interpretations per acronym.

```py
>>> from acronymer import generate_acronym_interpretations
>>> output = generate_acronym_interpretations("API, CPU", "tech terms", n=2)
>>> print(output)
Acronym: API  
Interpretations:  
1. Application Programming Interface  
2. Advanced Performance Integration  

Acronym: CPU  
Interpretations:  
1. Central Processing Unit  
2. Computational Processing Unit
```


```py
>>> output = generate_acronym_interpretations("API, CPU", "dragon names", n=2)
>>> print(output)
Acronym: API  
Interpretations:  
1. Arcane Power Infuser  
2. Aetherial Presence Instigator  

Acronym: CPU  
Interpretations:  
1. Celestial Pulse Unleasher  
2. Chaos-Proto Urge
```

### Generate Acronyms for Context

Generates a list of acronyms with creative full-form interpretations tailored to a given context.

_Doctest Example:_

```py
>>> from acronymer import generate_acronyms_for_context
>>> output = generate_acronyms_for_context("A software package that has tools for acronyms", max_letters=3, num_acronyms=4)
>>> print(output)
1. Acronym: APT  
   Interpretation: Acronym Projection Tools  

2. Acronym: CAT  
   Interpretation: Creative Acronym Toolkit  

3. Acronym: MAP  
   Interpretation: Meaningful Acronym Producer  

4. Acronym: TAP  
   Interpretation: Text Acronym Processor
```

## Functions

- **generate_acronym_interpretations(acronyms, context, n=1)**  
  Generate creative and context-specific interpretations for each acronym.

- **generate_acronyms_for_context(context, max_letters=4, num_acronyms=5)**  
  Generate a list of acronyms with creative interpretations based on the provided context.


