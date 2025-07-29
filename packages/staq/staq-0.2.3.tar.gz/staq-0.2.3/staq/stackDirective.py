from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util import (
    i18n,
    logging,
)

import os


from staq.stack import Stack
from staq.stackSession import StackSession
import yaml
import time 


class StackDirective(SphinxDirective):
    has_content = True

    optional_arguments = 1
    option_spec = {
        'file': directives.path,
        'baseaddress': directives.positive_int,
        'showaddresses': directives.unchanged,
        'width': directives.unchanged,
    }


    def run(self):
        env = self.state.document.settings.env
        base_address = self.options.get('baseaddress', 0xffff)
        show_addresses = self.options.get('showaddresses', 'true')
        width = self.options.get('width', '100%')

        if show_addresses.lower() == 'true':
            show_addresses = True
        else:
            show_addresses = False


        # Get the Sphinx builder
        builder = self.state.document.settings.env.app.builder.name
        session = StackSession()
        session.stack.setBaseAddress(base_address)

        contents = ""

        if self.arguments:

            fn = i18n.search_image_for_language(self.arguments[0], env)
            relfn, absfn = env.relfn2path(fn)
            filePath = absfn

            if not os.path.exists(filePath):
                error = nodes.error(None, nodes.paragraph(text=f"File not found: {filePath}"))
                return [error]

            with open(filePath, "r") as fh:
                contents = fh.read() + "\n"

        contents += '\n'.join(self.content)


        contentHash = str(abs(hash(contents)))
        output_dir = self.state.document.settings.env.app.outdir

        image_name = f"stack_{contentHash[:8]}.png"
        image_path = os.path.join(output_dir, image_name)
        #log_path = os.path.join(output_dir, "stack.log")

        # with open(log_path, "w") as fh:
        #     fh.write(f"content hash: {contentHash}\n")
        #     fh.write(f"image path: {image_path}\n")
        #     fh.write(f"builder: {builder}\n")
        #     fh.write(f"output dir: {output_dir}\n")
        #     fh.write(f"base address: {base_address}\n")
        #     fh.write(f"show address: {show_addresses}\n")
        #     fh.write(f"content: {contents}\n")

        for line in contents.split('\n'):
            session.parseCommand(line)

        if builder == 'html':
            html_content = session.stack.toHtml(showAddress= show_addresses, full=False)
            raw_html_node = nodes.raw('',html_content, format='html')
            return [raw_html_node]
        else:
    

            timeout = 10

            try:
                session.stack.generatePng(image_path, width=width)

                while not os.path.exists(image_path) and timeout > 0:
                    timeout -= 1
                    time.sleep(1)

                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"Image not generated: {image_path}\ntry again")
            except Exception as e:
                print(f"Error: {e}")
                error = nodes.error(None, nodes.paragraph(text=f"Error: {e}"))

                with open("error.log", "w") as fh:
                    fh.write(str(e))

                return [error]

            image_node = nodes.image(uri= f"/{image_path}")
            # image_node['width'] = width

            return [image_node]
        

    



def generate_stack_image(stack, base_address, show_addresses, env, contentHash):
    

    image_path = os.path.join(env.app.outdir, f"stack_{contentHash}.png")
    stack.generatePng(image_path)

    
    return image_path

def setup(app):
    app.add_directive('stack', StackDirective)

    return {'parallel_read_safe': True}
