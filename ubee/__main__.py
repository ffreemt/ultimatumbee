"""Gen main."""
import gradio as gr


def greet(name):
    """Dummy."""
    return "Hello " + name + "!!"


def main():
    """Create main entry."""
    title = "Ultimatumbee Aligner"
    theme = "dark-grass"
    description = """WIP showcasing a novel aligner"""
    article = \
        """Coming soon...
        """
    examples = [
        ["yo"],
        ["me"],
    ]

    iface = gr.Interface(
        fn=greet,
        title=title,
        theme=theme,
        description=description,
        article=article,
        inputs="text",
        outputs="text",
        examples=examples,
    )
    iface.launch(
        enable_queue=False
    )


if __name__ == "__main__":
    main()
