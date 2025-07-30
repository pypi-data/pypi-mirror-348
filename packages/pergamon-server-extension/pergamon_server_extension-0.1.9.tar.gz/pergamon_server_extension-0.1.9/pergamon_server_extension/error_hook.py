import traceback
from IPython.display import display, HTML
import os
import re

import ipywidgets as widgets
from IPython.core import ultratb
from ipykernel.comm import Comm

AI_MODEL = os.environ.get("CALLIOPE_ERROR_MODEL", "gpto")

def custom_exc(shell, etype, evalue, tb, tb_offset=None):
    error_message = str(evalue)
    error_type = etype.__name__    
    error_line = None
    try:
        for frame in traceback.extract_tb(tb):
            if frame.filename.startswith('<ipython-input-'):
                error_line = frame.lineno
                break
    except:
        pass
    
    current_cell = shell.user_ns.get('_ih', [""])[len(shell.user_ns.get('_ih', [""])) - 1]
    
    display(HTML(f"""
        <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border: 1px solid #f5c6cb; border-radius: 5px; margin: 10px 0;">
            <h3 style="margin-top: 0;">{error_type} Error Detected</h3>
            <p><strong>Error:</strong> {error_message}</p>
            <p><strong>Line:</strong> {error_line if error_line is not None else 'unknown'}</p>
        </div>
    """))

    button_style = widgets.ButtonStyle(
        button_color='#3FF1EF',
        text_color='#161D2C'
    )

    fix_button = widgets.Button(
        description="Fix with Calliope",
        tooltip='Get AI to fix your code',
        icon='check',
        style=button_style
    )
    
    show_error_button = widgets.Button(
        description="Show Traceback",
        tooltip='Show the full error traceback',
        icon='bug',
        style=button_style
    )
    
    button_container = widgets.HBox([fix_button, show_error_button])
    display(button_container)
    
    output_area = widgets.Output()
    display(output_area)

    def on_fix_click(b):
        with output_area:
            output_area.clear_output()
            Comm(target_name='toggle_fixing').send({})
            display(HTML("""
            <div style="padding: 10px; margin: 5px 0; display: flex; align-items: center;">
                <span>Calliope is fixing your code, please wait...</span>
            </div>
            """))
            
            ai_prompt = f"""\
            Please fix the following Python code that resulted in a {error_type} error: {error_message}
            
            ---CODE WITH ERROR---
            {current_cell}
            ---END CODE---
            
            Provide ONLY the fixed code without any explanations or markdown formatting. The error occurred on line {error_line if error_line is not None else 'unknown'}.
            """
            
            ai_magic = f"%%ai {AI_MODEL} \n{ai_prompt}"
            res = shell.run_cell(ai_magic)
            fixed_code = None
            
            if hasattr(res.result, '_repr_markdown_'):
                markdown_content = res.result._repr_markdown_()
                code_blocks = re.findall(r'```(?:python)?\n(.*?)```', markdown_content[0], re.DOTALL)
                if code_blocks:
                    fixed_code = code_blocks[0].strip()
                else:
                    fixed_code = markdown_content.strip()
            
            output_area.clear_output()

            Comm(target_name='toggle_fixing').send({})
            if fixed_code:
                apply_fix_button = widgets.Button(
                    description="Apply Fix",
                    tooltip='Apply the fixed code to your cell',
                    icon='check-circle',
                    style=button_style
                )
                
                display(HTML(f"""
                <div style="padding: 15px; margin: 10px 0;">
                    <h3 style="margin-top: 0;">Fix Generated</h3>
                    <p>A fix has been generated. Click the button below to apply it to your cell.</p>
                </div>
                """))
                
                preview_accordion = widgets.Accordion(children=[widgets.HTML(
                    value=f'<pre style="padding: 10px; overflow: auto; white-space: pre-wrap; font-family: monospace;">{fixed_code.replace("<", "&lt;").replace(">", "&gt;")}</pre>'
                )])
                preview_accordion.set_title(0, 'Preview Fixed Code')
                                
                display(preview_accordion)
                display(apply_fix_button)
                
                def on_apply_fix(b):
                    with output_area:
                        output_area.clear_output()                        
                        comm = Comm(target_name='replace_cell')
                        comm.send({'replace_with': fixed_code, 'execute_cell': True})
                apply_fix_button.on_click(on_apply_fix)
            else:
                display(HTML(f"""
                <div style="background-color: #172134; color: #721c24; padding: 15px; margin: 10px 0;">
                    <h3 style="margin-top: 0;">Unable to Fix</h3>
                    <p>Calliope was unable to generate fixed code automatically.</p>
                </div>
                """))

    def on_show_error_click(b):
        with output_area:
            output_area.clear_output()
            formatter = ultratb.FormattedTB(mode='Context', color_scheme='Linux')
            formatted_tb = formatter.text(etype, evalue, tb)
            
            display(HTML(f"""
            <div style="padding: 15px; margin: 10px 0;">
                <h3 style="margin-top: 0;">Error Traceback:</h3>
                <pre style="padding: 10px; overflow: auto; white-space: pre-wrap;">{formatted_tb.replace('<', '&lt;').replace('>', '&gt;')}</pre>
            </div>
            """))

    fix_button.on_click(on_fix_click)
    show_error_button.on_click(on_show_error_click)

    return None

def load_ipython_extension(ipython):
    ipython.set_custom_exc((Exception,), custom_exc)

def unload_ipython_extension(ipython):
    ipython.set_custom_exc((), None)