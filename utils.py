
def _extract_and_print_pdb_and_property(model, user_input) -> list:
    # Get the PDB ID
    response = model.generate_content(f'Can you extract the PDB ID from this input: {user_input}')
    pdb_id = response.text

    if len(pdb_id) != 4:
        print("Cannot find PDB ID! Let's start again")
        return pdb_id, None

    # Get property
    response = model.generate_content(f'Can you extract the property to be calculated from this input: {user_input}')
    prop = response.text

    response = model.generate_content(f'Can you extract the chain to be used from this input: {user_input}')
    chain_id = response.text

    ## Check if PDB ID and property are correct
    print(f"MSC: The PDB ID I am looking up is '{pdb_id}', and I am calculating the '{prop}' for chain '{chain_id}'. Does that sound ok?")

    return pdb_id, prop, chain_id

def _check_affirmative(model, user_input) -> bool:
    if user_input.lower() == 'no':
        return False

    # Ask model if response is affirmative
    response = model.generate_content(f'Is this response affirmative? Say True or False: {user_input}')

    if response.text.lower() == 'true':
        return True
    
    return False

def _continue_chat(user_input):
    if user_input.lower() == 'quit':
        return False
    
