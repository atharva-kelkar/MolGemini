import requests

def _download_pdb(pdb_id, save_path):
    """Function to download pdb"""
    # Construct the URL for the PDB file
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    # Send a GET request to download the file
    response = requests.get(pdb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content to a file
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {pdb_id}.pdb")
    else:
        print(f"Failed to download {pdb_id}.pdb")

def remove_markdown_code_blocks(text):
    """Function to remove markdown from generated code"""
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if not line.strip().startswith('```')]
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text

def _write_code_for_property_and_file(
        model, 
        pdb_file, 
        property_to_calculate, 
        chain_id, 
        n_trial=0, 
        n_max_attempts=8
        ):
    """Function to write code for the specified property and file"""
    try:
        if n_trial <= n_max_attempts:
            # Make check prompt 
            analysis_check_prompt = 'Which pdb has been provided? Which property should be computed? For which chain?'
            analysis_check = model.generate_content([analysis_check_prompt, pdb_file, property_to_calculate, chain_id])

            # Make analysis prompt
            # analysis_prompt=f'Please write code using MDAnalysis to perform the computation for the PDB file {pdb_file}'\
            #      + f'and property {property_to_calculate}, for all chains'
            analysis_prompt = 'Please write code using MDTraj to perform the computation for the given PDB, Property, and chain ID.'\
                + 'Print output as "The value of the property is..." and rounded up to 3 decimal places.'
            # analysis_prompt = 'Write a function using MDAnalysis to use a given PDB file to return the given property, selecting all atoms.'
            # Write code
            pdb_analysis = model.generate_content(
                [
                    analysis_prompt, 
                    analysis_check.text
                ]
            )
            # Convert code to proper format
            analysis_code = remove_markdown_code_blocks(pdb_analysis.text)
            # print(analysis_code)
            # Execute and return output of function
            exec(analysis_code)
            # print(analysis_code)
            # Return output
            # return output
            # elif n_trial > n_max_attempts:
            #     return None
            print('*** Analysis completed for this request ***\n\n ~~~ New request begins ~~~\n\n')
    except:
        _write_code_for_property_and_file(
            model, 
            pdb_file, 
            property_to_calculate,
            chain_id, 
            n_trial=n_trial+1
        )

def _make_good_output(model, pdb_id, property_to_calculate, output):
    """Function to take property and make a decent output using Gemini"""
    if output == None:
        print('Sorry, we could not generate output as asked by you')
    else:
        prompt = "Make a response for the following PDB ID and property to give to the user with the given output"
        output = model.generate_content([prompt, pdb_id, property_to_calculate, output])
        print(output.text)    




