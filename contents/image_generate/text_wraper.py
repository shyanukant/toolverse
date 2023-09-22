from PIL import Image, ImageFont


def wrap_text(text, font, max_width):
    # Initialize an empty list of lines
    lines = []

    # Split the text by whitespace
    words = text.split()

    # Initialize an empty line
    line = ""

    # Loop through the words
    for word in words:
        # Add the word to the line with a space
        line += word + " "

        text_left, text_upper, text_right, text_lower = font.getbbox(line)
    
        line_width = text_right - text_left
        line_height = text_lower - text_upper
        # Get the size of the line with the font

        # Check if the line exceeds the max width
        if line_width > max_width:
            # Remove the last word and space from the line
            line = line[:-len(word) - 1]

            # Append the line to the list of lines
            lines.append(line)

            # Start a new line with the word
            line = word + " "

    # Append the last line to the list of lines
    lines.append(line)

    # Return the list of lines
    return lines
