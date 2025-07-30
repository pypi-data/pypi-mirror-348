import io
import logging
from plotly.graph_objs import Figure

logger = logging.getLogger(__name__)

def bytes_from_figure(f: Figure, **kwargs) -> bytes:
    """
    Convert a Plotly Figure to a PNG image as bytes.

    Args:
        f (Figure): The Plotly Figure object to be converted.

    Returns:
        bytes: The PNG image data as bytes.
        :param f:  The Plotly Figure object to be converted into a PNG image.
    """

    format_file = kwargs.get("format_file", "png")  # The format of the image to be converted to
    width = kwargs.get("width", 640)  # The width of the image in pixels
    height = kwargs.get("height", 480)  # The height of the image in pixels

    with io.BytesIO() as bytes_buffer:
        f.write_image(bytes_buffer, 
                      format=format_file, 
                      width = width, 
                      height = height)  # Write the figure to the bytes buffer as a PNG image
        bytes_buffer.seek(0)  # Reset the buffer position to the beginning
        return bytes_buffer.getvalue()  # Return the bytes data

def html_from_figure(f: Figure) -> str:
    """
    Convert a Plotly Figure to an HTML string.

    Args:
        f (Figure): The Plotly Figure object to be converted.

    Returns:
        str: The HTML representation of the figure as a string.
    """
    with io.BytesIO() as bytes_buffer:
        # Wrap the BytesIO with a TextIOWrapper to handle strings
        with io.TextIOWrapper(bytes_buffer, encoding='utf-8') as text_buffer:
            f.write_html(text_buffer)  # Write the figure to the text buffer
            text_buffer.flush()  # Ensure all data is written
            bytes_buffer.seek(0)  # Reset the buffer position to the beginning
            return bytes_buffer.getvalue().decode('utf-8')  # Decode bytes to string and return
