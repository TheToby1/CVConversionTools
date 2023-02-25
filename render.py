import git
import os
import shutil
import tempfile
import argparse
from mistletoe import Document
from mistletoe_extension.blazor_renderer import MudBlazorCVRenderer
from mistletoe_extension.moderncv_renderer import ModernCVRenderer
from mistletoe_extension.json_renderer import JsonCVRenderer
# Currently this renders the given file to all possible outputs, I should add a second arg for the output type.

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def get_file_from_git(gitDir, filePath):
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    # Create temporary dir
    t = tempfile.mkdtemp()
    # Clone into temporary dir
    git.Repo.clone_from(gitDir, t, branch='main', depth=1)
    # Copy desired file from temporary dir
    shutil.move(os.path.join(t, filePath), os.path.join('./temp', os.path.basename(filePath)))
    # Remove temporary dir
    shutil.rmtree(t, onerror=onerror)

def render_file(filePath, outFileName):
    rendered = None
    if not os.path.exists('./output'):
        os.mkdir('./output')

    with open(filePath, 'r') as fin:
        with ModernCVRenderer() as renderer:
            rendered = renderer.render(Document(fin))

    with open(os.path.join('./output', outFileName + '.tex'), 'w') as fout:
        fout.write(rendered)

    rendered_html = None
    with open(filePath, 'r') as fin:
        with MudBlazorCVRenderer() as renderer:
            rendered_html = renderer.render(Document(fin))

    with open(os.path.join('./output', outFileName + '.razor'), 'w') as fout:
        fout.write(rendered_html)

    rendered_json = None
    with open(filePath, 'r') as fin:
        with JsonCVRenderer() as renderer:
            rendered_json = renderer.render(Document(fin))

    with open(os.path.join('./output', outFileName + '.json'), 'w') as fout:
        fout.write(rendered_json)

def get_file_and_render(input_file, git_dir='', output_file='output'):
    if git_dir != '':
        get_file_from_git(git_dir, input_file)
        input_file = os.path.join('./temp', os.path.basename(input_file))
    
    render_file(input_file, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renders the given md file as a modernCV tex file and a blazor file.')
    parser.add_argument('-i','--input-file', help='Input md file path', required=True)
    parser.add_argument('-g','--git-dir', help='Git directory to pull file from', required=False)
    parser.add_argument('-o','--output-file', help='Name of output file', required=False)
    args = vars(parser.parse_args())
    not_none_args = {k:v for k, v in args.items() if v is not None}
    get_file_and_render(**not_none_args)