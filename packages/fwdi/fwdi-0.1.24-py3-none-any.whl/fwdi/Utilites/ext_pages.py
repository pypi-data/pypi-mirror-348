from datetime import datetime
import gradio as gr
from fwdi.Domain.Session.session_state import SessionState
from fwdi.Utilites.ext_gradio_request import ExtGradioRequest

class ExtPages():
    def __get_session_hash(self, session_state:SessionState, request:gr.Request):
        current_session = ExtGradioRequest.get_or_create_user_session(session_state, request)
        current_session.user_data['start_at'] = f"first_in:{datetime.now()}"
        status_txt = gr.Markdown(value=f"Session id: {current_session.session_id}", label="Status text:")
        
        return status_txt, session_state