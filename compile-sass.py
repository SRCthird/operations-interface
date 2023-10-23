import sass
import glob
import os

# Search for all .scss files in the project
scss_files = glob.glob('**/*.scss', recursive=True)

for scss in scss_files:
    # Create the output CSS file path
    output_css = scss.replace('scss', 'css')

    # Ensure the output CSS directory exists
    os.makedirs(os.path.dirname(output_css), exist_ok=True)

    # Compile the SCSS file to CSS
    compiled_css = sass.compile(filename=scss)

    # Save the compiled CSS to a file
    with open(output_css, 'w') as f:
        f.write(compiled_css)

    print(f'{scss} => {output_css}')
