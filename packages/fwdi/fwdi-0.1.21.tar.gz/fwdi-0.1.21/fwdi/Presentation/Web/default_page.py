import gradio as gr

from ...Application.Abstractions.base_panel import BaseWebPage

class DefaultPage(BaseWebPage):

    def create_panel(self)->gr.Blocks:
        with gr.Blocks() as demo:
            gr.Markdown("""# Default Web page.
### Here you can locate all kinds of information about the current microservice:
- Text
- Document
- Image
- Video
- Audio files
- Settings""")
            
        return demo