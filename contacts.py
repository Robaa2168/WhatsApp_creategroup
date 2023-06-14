import vobject

# Open and read the vcf file
with open('A38.vcf', 'r') as f:
    vcf_text = f.read()

# Initialize a counter
i = 1

# Initialize a list to store the modified vcards
modified_vcards = []

# Parse the vcf file and loop over the vcards
for vcard in vobject.readComponents(vcf_text):
    # Create a new name
    new_name = 'Kamau' + str(i)
    
    # Change the name
    vcard.remove(vcard.n)
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=new_name, given=new_name)

    # Change the formatted name
    vcard.remove(vcard.fn)
    vcard.add('fn')
    vcard.fn.value = new_name

    # Print the change
    print(f'{new_name} saved')

    # Add the modified vcard to the list
    modified_vcards.append(vcard)

    # Stop after 300 contacts
    if i >= 300:
        break

    # Increment the counter
    i += 1

# Write the vcf file
with open('contacts.vcf', 'w') as f:
    for vcard in modified_vcards:
        f.write(vcard.serialize())
