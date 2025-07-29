"""
Acronym Tools

"""
import oa

def generate_acronym_interpretations(acronyms, context, n=1):
    """
    Generate {n} interpretations for each acronym based on the provided context.
    
    Args:
        acronyms (str): A string of acronyms separated by spaces or commas.
        context (str): The context to guide the acronym interpretations.
        n (int): Number of interpretations per acronym.
        
    Returns:
        str: The generated interpretations.
    
    Example:
        >>> output = generate_acronym_interpretations("API, CPU", "tech terms", n=2)  # doctest: +SKIP
        >>> print(output)  # doctest: +SKIP
        Acronym: API  
        Interpretations:  
        1. Application Programming Interface  
        2. Advanced Performance Integration  
        <BLANKLINE>
        Acronym: CPU  
        Interpretations:  
        1. Central Processing Unit  
        2. Computational Processing Unit  

        >>> output = generate_acronym_interpretations("API, CPU", "dragon names", n=2)  # doctest: +SKIP
        >>> print(output)  # doctest: +SKIP
        Acronym: API  
        Interpretations:  
        1. Arcane Power Infuser  
        2. Aetherial Presence Instigator  
        <BLANKLINE>
        Acronym: CPU  
        Interpretations:  
        1. Celestial Pulse Unleasher  
        2. Chaos-Proto Urge  
    """
    template = """
You are a creative acronym generator. Given a list of acronyms and a specific context, generate {n} full-form interpretations for each acronym. Each interpretation must be consistent with the context and expand the acronym creatively.

Acronyms: {acronyms}  
Context: {context}  
Number of interpretations per acronym: {n}

Output format:
Acronym: <ACRONYM>
Interpretations:
1. <Interpretation 1>
2. <Interpretation 2>
...
"""
    try:
        func = oa.prompt_function(template)
        response = func(acronyms=acronyms, context=context, n=n)
        return response
    except Exception as e:
        return f"Error generating interpretations: {e}"

def generate_acronyms_for_context(context, max_letters=4, num_acronyms=5):
    """
    Generate a list of acronyms and a creative full-form interpretation for each tailored to the given context.
    
    Args:
        context (str): The context to guide acronym creation.
        max_letters (int): Maximum number of letters per acronym.
        
    Returns:
        str: The generated acronyms with their full-form interpretation.
    
    Example:
        >>> output = generate_acronyms_for_context("A software package that has tools for acronyms", max_letters=3, num_acronyms=4)
        >>> print(output)  # doctest: +SKIP
        1. Acronym: APT  
        Interpretation: Acronym Projection Tools  
        <BLANKLINE>
        2. Acronym: CAT  
        Interpretation: Creative Acronym Toolkit  
        <BLANKLINE>
        3. Acronym: MAP  
        Interpretation: Meaningful Acronym Producer  
        <BLANKLINE>
        4. Acronym: TAP  
        Interpretation: Text Acronym Processor  

    """
    template = """
You are an expert in creating meaningful acronyms. Generate a list of acronyms, each with a 
creative full-form interpretation that aligns with the following context.

Context: {context}  
Maximum letters per acronym: {max_letters}
Number of acronyms: {num_acronyms}

Provide the output as a list of acronyms and their corresponding interpretation.

Format:
Acronym: <ACRONYM>
Interpretation: <Full-form>
"""
    try:
        func = oa.prompt_function(template)
        response = func(context=context, max_letters=max_letters, num_acronyms=num_acronyms)
        return response
    except Exception as e:
        return f"Error generating acronyms: {e}"
