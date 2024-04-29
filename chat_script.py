import json
import requests
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
from utils import _continue_chat, _extract_and_print_pdb_and_property, _check_affirmative
from pdb_helper import _download_pdb, _write_code_for_property_and_file, _make_good_output

def chat(model):
    print("Welcome to MolGemini (MG)!")
    print("Type 'quit' to exit.")
    ## Dummy user input
    user_input = 'init'

    while True:
        # Check if user wants to quit
        if user_input.lower() == 'quit':
            print("MolGemini: Goodbye!")
            break

        while True:
            ## Generate initial prompt for PDB ID and property
            print("\nMolGemini: Please provide a PDB ID and property of interest to you, and chain ID for which the property is to be calculated.")

            ## Get user input
            user_input = input("You: ")
            if _continue_chat(user_input) is False: break

            ## Extract PDB ID and property from user input
            pdb_id, property_to_calculate, chain_id = _extract_and_print_pdb_and_property(model, user_input)

            ## Take user response
            user_input = input("You: ")
            if _continue_chat(user_input) is False: break

            ## Break out of loop if not affirmative
            if not _check_affirmative(model, user_input):
                print("I did not get the correct PDB ID or property. Let's try again!")
                continue
            
            print("MolGemini: Do you also want me to print the code I used for the analysis?")

            ## Take user response
            user_input = input("You: ")
            if _continue_chat(user_input) is False: break

            ## Store whether code is to be shown to user
            to_show_code = _check_affirmative(model, user_input)

            # Confirm calculation
            print("MolGemini: Great! Downloading PDB file...")
            pdb_file = f'{pdb_id}.pdb'
            _download_pdb(pdb_id, pdb_file)

            print("MolGemini: Calculating property...")
            output = _write_code_for_property_and_file(
                model,
                pdb_file,
                property_to_calculate,
                chain_id,
		to_show_code=to_show_code,
            )
            # _make_good_output(model, pdb_id, property_to_calculate, output)

            # Check if user wants to quit
            if user_input.lower() == 'quit':
                print("MolGemini: Goodbye!")
                break


if __name__ == "__main__":
    # Instantiate model
    model = GenerativeModel(model_name="gemini-1.0-pro-vision")

    chat(model)
