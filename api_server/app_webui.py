import gradio as gr

from app import main


def greet(name):
    response_text, _ = main(name)
    return response_text + "\n" + str(_)


# We instantiate the Textbox class
textbox = gr.Textbox(label="Type your query", placeholder="Anything you want to ask", lines=2)

gr.Interface(fn=greet, inputs=textbox, outputs="text").launch(server_port=11990)