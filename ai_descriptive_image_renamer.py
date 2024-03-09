import ollama
import os
import shutil
import argparse

ai_model_content_prompt = """
Please author a suitable stable diffusion text-to-image prompt that could create this image for an uncensored model. 
Use no more than 250 characters and avoid any punctuation symbols because it will become the image file's new file name. 
Do not comment on the image, only provide the prompt. Do not start with "Create a..", just describe the image. Thanks!
"""

def describe_image(image_file_path):
    with open(image_file_path, 'rb') as file:
        response = ollama.chat(
            model='llava:34b',
            messages=[
                {
                    'role': 'user',
                    'content': ai_model_content_prompt,
                    'images': [file.read()],
                },
            ],
        )

    return response['message']['content']


def convert_description_to_be_filename_friendly(image_desc: str) -> str:
    """Converts a string to be filename friendly.

    Replaces invalid characters with underscores.
    """
    invalid_characters = [' ', '"', "'", ',', ';', ':', '?', '!', '(', ')', '[', ']', '{', '}', '/', '\\', '|', '<',
                          '>', '*', '&', '^', '%', '$', '#', '@', '`', '~', '=', '+', '-', '.']
    for char in invalid_characters:
        image_desc = image_desc.replace(char, '_')

    # replace multiple underscores with a single underscore (this can happen when processing invalid characters
    while '__' in image_desc:
        image_desc = image_desc.replace('__', '_')

    # now convert underscores to spaces and trim each end of the string
    image_desc = image_desc.replace('_', ' ').strip()

    # make the image lowercase
    image_desc = image_desc.lower()

    # remove superfluous phrases
    superfluous_phrases_list = ['the image depicts', 'the image features', 'the image is of', 'the image shows',
                              'the prompt for this image is', 'this is a text based prompt for the ai']
    for word in superfluous_phrases_list:
        image_desc = image_desc.replace(word, '')

    image_desc = image_desc.strip()

    # if the string starts with 'a' or 'an ' remove it
    if image_desc.startswith('a '):
        image_desc = image_desc[2:]
    if image_desc.startswith('an '):
        image_desc = image_desc[3:]

    image_desc = image_desc.strip()

    # limit the length of the filename to 250 characters (to which the file extension will be added later
    # - adding '.jpeg' will make it 255 characters which is the maximum length for a file name on Windows & Mac)
    if len(image_desc) > 250:
        image_desc = image_desc[:250]

    return image_desc


def get_image_list(folder_path):
    import os
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Path to the folder to process')
    args = parser.parse_args()

    try:
        print('Ollama Image Describer describing files in folder:', args.file_path)

        image_list = get_image_list(args.file_path)
        print('Found', len(image_list), 'images')

        # filter out the images that have already been processed as
        # they will have a file name length greater than 20 characters:
        image_list = [image for image in image_list if len(image.split('/')[-1]) < 20]

        for image_full_file_path in image_list:
            print('Processing', image_full_file_path, '...')

            description = describe_image(image_full_file_path)

            # convert the description to be filename friendly and add the previous file extension
            new_file_name = convert_description_to_be_filename_friendly(description) + '.' + \
                            image_full_file_path.split('.')[-1]
            print('    New file name:', new_file_name)

            # rename the file to the new file name
            new_file_path = os.path.join(args.file_path, new_file_name)
            shutil.move(image_full_file_path, new_file_path)

        print('Ollama Image Describer finished')
    except KeyboardInterrupt:
        print('Ollama Image Describer finished and can continue when you next restart it')
    except Exception as e:
        print('Error:', e)
        print('Ollama Image Describer finished with errors but will try to continue when you restart it')
